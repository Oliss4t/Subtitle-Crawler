#### 1. Use and understand **Git!** ####
Look around here in the version control ;)
#### 2. **UML** at least **3** good diagrams. "good" means you can pump it up artificially as written in DDD. You have 10 million $ from me! Please export the pics. I can not install all tools to view them! ####
I modelled the following three diagrams:
- The Use Case Diagram shows the use interations with the Movie Learning App. There are no other Actors execpt the "Background Syste" which ensures the data preparation process. 
  - [Use Case Diagram](UML/use_case_diagram.svg)
- The Deployment Diagram shows the physical deployment of the Movie Learning App. The App has three diffrent client versions. One Webapp, one Desktopapp and one for the native mobile devices. The Backand consists of multiple services. The main services are the "Learning Service" which covers the tracking of the learned vocabs for a user and a movie and the "User Service" which handles the authentification/registration as well as the subscriptions of the users. The backend also fetches data from the three APIs: TranslationAPI, SubtitleAPI and IMDBAPI.
  - [Deployment Diagram](UML/deployment_diagram.svg)
- The Activity Diagram shows the workflow of the learning process. A user starts by logging in, selecting whether he wants to learn offline or online and then starts the actual learning process. 
  - [Activity Diagram](UML/activity_diagram.svg)

#### 3. **DDD** If your domain is too small, invent other domains around and document these domains (as if you have 10 Mio € from Edlich-Investment!) Develop a clear strategic design with mappings/relationships with 5-0 Domains. It would be nice if these domains are derived from an Event-Storming (but not mandatory). ####
I started the DDD approach by doing a event storming to figure out all domain events and therefore all domains for my app. Then I combined the related subdomains to the larger domains and modeled their relationships. Furthermore I created the core domain chart and placed every domain in their category (core, supporting or generic).
- [Event Storming](DDD/event_storming_domains.pdf)
- [Domain and Subdomain Relationships](DDD/domains_and_sub_domains_core_domain_chart.pdf)
- [Core Domain Chart](DDD/domains_and_sub_domains_core_domain_chart.pdf)
#### 4. **Metrics** at least two. Sonarcube would be great. Other non trivial metrics are also fine. ####
#### 5. **Clean Code Development:** at least **5** points you can show me + >>10 points on your **personal cheat sheet** ####
#### 6. **Build Management** with any Build System as Ant, Maven, Gradle, etc. (only Travis is perhaps not enough) Do e.g. generate Docs, call tests, etc. ####
#### 7. Integrate some nice **Unit-Tests** in your Code to be integrated into the Build ####
#### 8. **Continuous Delivery:** show me your pipeline in e.g. Jenkins, Travis-CI, Circle-CI, GitHub Action, GitLab CI, etc. ####
#### 9. Use a good **IDE** and get fluent with it as e.g. IntelliJ. What are your favorite **Key-Shortcuts**?! ####
#### 10. **DSL** Create a small DSL Demo example snippet in your code even if it does not contribute to your project ####
#### 11. **Functional Programming** (prove that you have covered all functional aspects in your code as ####
####  - only final data structures ####
####  - (mostly) side effect free functions ####
####  - the use of higher-order functions ####
####  - functions as parameters and return values ####
####  - use closures / anonymous functions ####
