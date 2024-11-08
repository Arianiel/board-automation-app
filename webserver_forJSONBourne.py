from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import str
import json
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from github_interactions import automation_information, update_item_info

import tornado.ioloop
import tornado.web
import asyncio

from external_webpage.request_handler_utils import get_detailed_state_of_specific_instrument, \
    get_summary_details_of_all_instruments, get_instrument_and_callback
from external_webpage.web_scrapper_manager import WebScrapperManager
from external_webpage.instrument_scapper import scraped_data, scraped_data_lock

logger = logging.getLogger('JSON_bourne')
log_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'log', 'JSON_bourne.log')
handler = TimedRotatingFileHandler(log_filepath, when='midnight', backupCount=30)
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# use dataweb2.isis.rl.ac.uk / ndaextweb3-data.nd.rl.ac.uk (130.246.92.89)
HOST, PORT = '130.246.92.89', 443

class MyHandler(tornado.web.RequestHandler):
    """
    Handle for web calls for Json Borne
    """

    def get(self):
        """
        This is called by BaseHTTPRequestHandler every time a client does a GET.
        The response is written to self.wfile
        """
        path = self.request.uri
        instrument = "Not set"
        try:
            instrument, callback = get_instrument_and_callback(path)

            # Debug is only needed when debugging
            logger.debug("Connection from {} looking at {}".format(self.request.remote_ip, instrument))

            with scraped_data_lock:
                if instrument == "ALL":
                    ans = {
                        "error": web_manager.instrument_list_retrieval_errors(),
                        "instruments": get_summary_details_of_all_instruments(scraped_data)}

                else:
                    ans = get_detailed_state_of_specific_instrument(instrument, scraped_data)

            try:
                ans_as_json = str(json.dumps(ans))
            except Exception as err:
                raise ValueError("Unable to convert answer data to JSON: {}".format(err))

            response = "{}({})".format(callback, ans_as_json)

            self.set_status(200)
            self.set_header('Content-type', 'text/html')
            self.write(response.encode("utf-8"))
        except ValueError as e:
            logger.exception("Value Error when getting data from {} for {}: {}".format(
                self.request.remote_ip, instrument, e))
            self.set_status(400)
        except Exception as e:
            logger.exception("Exception when getting data from {} for {}: {}".format(
                self.request.remote_ip, instrument, e))
            self.set_status(404)

    def log_message(self, format, *args):
        """ By overriding this method and doing nothing we disable writing to console
         for every client request. Remove this to re-enable """
        return


if __name__ == '__main__':
    # It can sometime be useful to define a local instrument list to add/override the instrument list do this here
    # E.g. to add local instrument local_inst_list = {"LOCALHOST": ("localhost", "MYPVPREFIX")}
    local_inst_list = {}
    web_manager = WebScrapperManager(local_inst_list=local_inst_list)
    web_manager.start()

    # As documented at https://github.com/tornadoweb/tornado/issues/2608
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        application = tornado.web.Application([
            (r"/", MyHandler),
        ])
        http_server = tornado.httpserver.HTTPServer(application, ssl_options={
            "certfile": r"C:\Users\ibexbuilder\dataweb2_isis_rl_ac_uk.crt",
            "keyfile": r"C:\Users\ibexbuilder\dataweb2_isis_rl_ac_uk.key",
        })
        http_server.listen(PORT, HOST)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("Shutting down")
        web_manager.stop()
        web_manager.join()
