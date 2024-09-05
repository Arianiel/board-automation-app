# Automation for ISIS Experiment Controls GitHub projects

# Purpose
There are a number of things related to project management of projects wihin GitHub which can be automated.

This repository contains those specifically used by the Experiment Controls Group at ISIS Pulsed Neutron and Muon Source.

# To use
This is a flask application, which will need to be run on an appropriate server.

Configuration information is detailed in the [Configuration Readme](/config_info/config_readme.md).

# Graph QL Naming Convention Used
Within graph_ql_queries simple queries are in camel case (camelCase) whilst mutations, which make changes to the projects, repositories, or issues are in Pascal case (PascalCase).
This convention is simply to make it clearer at a glance whether the ql query in use should be making changes or not.

