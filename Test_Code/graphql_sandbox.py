import requests

issues_query = """query {
  repository(owner:"Arianiel", name:"issues-repo") {
    issues(last:20) {
      edges {
        node {
          title
          url
          labels(first:5) {
            edges {
              node {
                name
              }
            }
          }
        }
      }
    }
  }
}"""


headers = {"Authorization": "token "+open("token", "r").read()}


def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


result = run_query(issues_query) # Execute the query
print(result)
