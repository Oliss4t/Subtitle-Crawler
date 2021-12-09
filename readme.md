Explanation of the project:
Command line tool for downloading subtitles and additional information regarding the movie

Installation:

Commands:
access help: python main.py --help

config
download -ml/-m -a -s -i -d
status


#### 1. Use and understand **Git!** ####
Look around here in the version control ;)
#### 2. **UML** at least **3** good diagrams. "good" means you can pump it up artificially as written in DDD. You have 10 million $ from me! Please export the pics. I can not install all tools to view them! ####
I modelled the following three diagrams:
- The Use Case Diagram shows the use interactions with the Movie Learning App. There are no other actors except the "Background System" which ensures the data preparation process. 
  - [Use Case Diagram](documentation/uml/use_case_diagram.svg)
- The Deployment Diagram shows the physical deployment of the Movie Learning App. The app has three different client versions. One webapp, one desktop app and one for the native mobile devices. The backend consists of multiple services. The main services are the "Learning Service" which covers the tracking of the learned vocabs for a user and a movie and the "User Service" which handles the authentifikation/registration as well as the subscription of the users. The backend also fetches data from the three APIs: TranslationAPI, SubtitleAPI and IMDBAPI.
  - [Deployment Diagram](documentation/uml/deployment_diagram.svg)
- The Activity Diagram shows the workflow of the learning process. A user starts by logging in, selecting whether he wants to learn offline or online and then starts the actual learning process. 
  - [Activity Diagram](documentation/uml/activity_diagram.svg)

#### 3. **DDD** If your domain is too small, invent other domains around and document these domains (as if you have 10 Mio € from Edlich-Investment!) Develop a clear strategic design with mappings/relationships with 5-0 Domains. It would be nice if these domains are derived from an Event-Storming (but not mandatory). ####
I started the DDD approach by doing a event storming to figure all domain events out and therefore all domains for my app. Then I combined the related subdomains to the larger domains and modeled their relationships. Furthermore I created the core domain chart and placed every domain in their category (core, supporting or generic).
- [Event Storming](documentation/ddd/event_storming_domains.pdf)
- [Domain and Subdomain Relationships](documentation/ddd/domains_and_sub_domains_core_domain_chart.pdf)
- [Core Domain Chart](documentation/ddd/domains_and_sub_domains_core_domain_chart.pdf)
#### 4. **Metrics** at least two. Sonarcube would be great. Other non trivial metrics are also fine. ####
I installed sonarqube and it concluded the follwing results. I didnt get it to work out the coverage, therefore i use the python coverage package:
- [Sonarqube Overview](documentation/metrics/sonarqube.PNG)
- 0 Bugs 
- 0 Vulnerabilities
- 7 Code Security Hotspots: After manual assessment, they are all no security vulerability. They are all http request to the opensubtitle [xmlrpc api](documentation/metrics/code_smell_example6.PNG). As to date there is not https api available.
- 15 Code Smells: After manual assessment the codesmells are also misleading: 
    - [abstract class](documentation/metrics/code_smell_example.PNG): the abstract class is with an pass statement defined in python
    - [method init](documentation/metrics/code_smell_example2.PNG): the init method had to many parameters, or the default definition if empty is not liked from sonarqube. Even        though it is completly vaild.
    - [empty code](documentation/metrics/code_smell_example3.PNG): i plan to keep on working on this project, therefore i left the method header 
    - [empty code](documentation/metrics/code_smell_example5.PNG)same reson for the out commented method 
- Debt of 1h 28min, mainly of the explained things in Code Smells
- [Coverage report: 76%](documentation/metrics/htmlcov/index.html) for the html to render the project needs to be downloaded.

#### 5. **Clean Code Development:** at least **5** points you can show me + >>10 points on your **personal cheat sheet** ####
Abstract Classes: to define the interface and so that we could switch out the opensubtitlescrapter with another scraper
#### 6. **Build Management** with any Build System as Ant, Maven, Gradle, etc. (only Travis is perhaps not enough) Do e.g. generate Docs, call tests, etc. ####
#### 7. Integrate some nice **Unit-Tests** in your Code to be integrated into the Build ####
I created 5 unit tests for the subtitle scraper. In unittests it is important that we are in a controlled environmet so that we can really test our one code.
But my scraper relies on fetching data and from external APIs, therefore i created several mock responses for unit testing. 
- [Mocks/Fixures](tests/subtitle_crawler/fixtures.py)
- [5 Unittests](tests/subtitle_crawler/test_download_subtitles.py)
#### 8. **Continuous Delivery:** show me your pipeline in e.g. Jenkins, Travis-CI, Circle-CI, GitHub Action, GitLab CI, etc. ####
#### 9. Use a good **IDE** and get fluent with it as e.g. IntelliJ. What are your favorite **Key-Shortcuts**?! ####
#### 10. **DSL** Create a small DSL Demo example snippet in your code even if it does not contribute to your project ####
#### 11. **Functional Programming** (prove that you have covered all functional aspects in your code as ####
####  - only final data structures ####
####  - (mostly) side effect free functions ####
####  - the use of higher-order functions ####
####  - functions as parameters and return values ####
####  - use closures / anonymous functions ####
