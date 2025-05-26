# Week 08 Software Architecture
## Outline
* What is a software architecture?
* Pipe and Filter
* Repository
* Blackboard
* Layered
* Also: Client Server; Process Control
* Design Documentation

## What is a software architecture?
1. Motivation: "As the size of software systems increases, the algorithms and data structures of the computation no longer constitute the major design problems. When **systems are constructed from many components**, the organisation of the overall system – **the software architecture – presents a new set of design problems**." — Shaw and Garlan (1994)
2. Why study Software architecture?
   * recognise common paradigms so you can
     * understand high level relationships among systems
     * build new systems as variations on existing ones
   * getting the right architecture is often crucial to the success of a design
     * the wrong architecture can lead to disastrous results
   * enable principled choices among design alternatives
   * architectural system representation is often essuential to analysis and description of high level properties of a complex system
4. Common Framework: All software architectures have **3** common elements:
   * **Components**: a software architecture consists of a collection of computational components
   * **Connectors**: the interactions between those components(e.g. procedure call, event broadcast, database, queries or pipes)
   * **Constraints**: a software architecture might have some constraints imposed on it(e.g. topogical constraint of having no cycles)

## Software Architecture
### 1. Pip and filter architecture structural pattern(similar called: "streams")
![image](https://github.com/user-attachments/assets/2373870c-31d6-4174-8cf4-d99cc74a975a)

1.1 Computational Model:
  * component - filter:
    ** reads streams of data on its inputs
    ** applies a local transformation
    ** produces streams of data on its outputs
  * computation is incremental:
    ** output begins before all inputs are consumed
  * connectors - pipes:
    ** transmit outputs of one filter to inputs of another

1.2 Essential Invariants 
  - Filters must be **independent** entities: They do not share states with other filters
  - Filters do not know the identity of other: upstream and downstream filters
  - Filter specifications can:
    - restrict what appears on the input pipes or
    - make guarantees about what appears on the output pipe
1.3 Examples:
  - Unix shell pipes: cat myfile.txt yourfile.txt | sort | more
  - Compilers: lexical analysis, parsing, semantic analysis, code generation
  - also used for: image and signal processing; functional programming; distributed systems

### 2. Repository architecture(Meybe comes up on the exam Recording:24:47)
![image](https://github.com/user-attachments/assets/7020b3de-00bd-4830-b45b-a26b6fd088dc)

2.1 How it works(Week 08 Lecture Recording 20:50): You can break down a problem into smaller bits you can post kind of work or problem into the repository and whenever one of these kind of knowledge agents sees something tgat it knows how to work, it can pull that off the board, work on it and post the results. It isn't really affected directly by any of the others.

2.2 Subsystems access and modify data from a  signal data structure; subsystems are loosely coupled (interact only through the repository)
;Two distinct types of components:

  - central data structure represents current state
  - independent components operate on the data store

2.3 Repository Interactions:

  - Control flow is dictated by central repository(triggers) or by the subsystems (lock, synchronization primitives)
  - Blackboard architecture interactions
      - current state of the central data structure is the main trigger
  - Traditioanl database interactions
      - input stream of transactions triggers selection of process to execute
   
2.4 Blackboard Repositories

  - Knowledge sources
    - separate, independent parcels of application-independent knowledge
  - Blackboard data structure
    - problem-solving state data organised in an application-dependent hierarchy
  - Control
    - driven by the state of the blackboard

2.5 Examples:

  - complex interpretations of signal processing: speech and pattern recognition
  - shared access to data with loosely coupled agents
  - some programming environments: collections of tools and shared repository of programs and program fragments
  - database management systems

### 3. Layering architecture
![image](https://github.com/user-attachments/assets/c09fe25f-15d9-411f-ba41-6e1735e86b26)

3.1 Model:

- hierarchical organisation: each layer
  - provides a services to the layer above
  - acts as a client to the layer below
- layers may either be
  - partially opaque(some interaction allowed between non-adjacent layers)
  - opaque: inner layers are hidden from all except the adjacent outer layer
 
3.2 Example:

- ISO reference model for Open Systems Interconnection(network protocols)
  - application layer
  - presentation
  - session
  - transport
  - network
  - data link
  - physical
 
3.3 Advantages:

  - Design based on increasing levels of abstraction
    - complex problem becomes sequence of incremental steps
  - Supports enhancement
    - changes to one layer affect at most two other layers
  - Supports reuse
    - different implementations of the same layer can be used interchangeably provided they support the same interfaces
   
3.4 Disadvantages:

  - Not all systems are easily structured in layers
  - Performance considerations: may need close coupling between logically high-level functions and their low-level implementations
  - Can be difficult to find right level of abstraction: e.g. protocols which bridge several OSI layers

### 4. Client and Server
![image](https://github.com/user-attachments/assets/e6959fe4-cb2d-4e14-b807-07c55d3ecb28)

4.1 Example:

  - Webservice: Laptops - Service

### 5. Process Control architecture(very rare, skip over)
![image](https://github.com/user-attachments/assets/df2806d1-7640-45f5-b0f4-28a0f3c1d301)


5.1 is also called "data flow". Example: Excel


# Design Documentation
1. Why write design documentation?

   - Explain your design choices to later developers
   - Ensure they don't duplicate research or work you have already done

2. Design documentation **records the design choices you made and reasons for them**. It records major choices made about the architecture of the system, and may contain design models(for instance, UML diagrams)
It is primarily written for architects, developers and maintainers

3. Other sorts of documentation:

   - User documentation: Written for end users and/or system administrators
   - API documentation: Written for internal, and possibly external, developers
   - Cookbooks/examples: Working code examples, written for developers

4. Some qualities of bad design documentation:

   - Hard to navigate: hard to find what you need
   - Out of date: no longer matches up with the current code
   - Incomplete/too little detail:  doesn't explain major decisions
   - Too much detail: major decisions are hidden in masses of unimportant detail
   - Never used: consumed time and effort on the part of the people who wrote it, but was never used
   - Contradictory: different portions of the documentation say contradictory things
   - Badly written/unclear: It is difficult for readers to understand what is meant
  
## Rationale
1. Rationale is the justification of decisions
2. Rationale is critical in two areas: it supports

   - decision making and
   - knowledge capture
3. Rationale is important when designing or updating the system and when introducing new staff
4. Rationale helps deal with change:

   - Improve maintenance support
      - Provide maintainers with design context
   - Improve learning
      - New staff can learn the design by replaying the decisions that produced it
   - Improve analysis and design
      - Avoid duplicate evaluation of poor alternatives
      - Make consistent and explicit trade-offs
5. Rationale activities - Rationale includes:

     - the issues that were addressed,
     - the alternative proposals which were considered,
     - the decisions made for resolution of the issues,
     - the criteria used to guide decisions and
     - the arguments developers went through to reach a decision
  
  6. Rationale Exercise:

     - Issue: How to realise database engine?
     - Proposals:
       - P1: use an Object Oriented database
       - P2: use a relational database
       - P3: use a file system
     - Arguments:
       - P1: use an Object Oriented database
         - A+ is able to ....
         - ......
       - P2: Use a relational DB
         - A+ offers a more robust engine....
         - .....
       - P3: Use a file system
         - ......
     - Criteria: Requirement to use CORBA
     - Resolution: Use a relational database(proposal P2), based on the criteria and in light of the relative simplicity of the system's persistent data relationships
    

  # Workshop
  ## Question 1
Question 1
The proposed E-mail Filter-o-Matic system is intended to filter incoming
e-mails. The following rules are applied to all incoming emails, in turn (if
any rules apply, no further rules are considered): emails are checked against a
whitelist (e-mails from senders on the whitelist are always accepted), a blacklist
(e-mails from senders on the blacklist are always deleted), and by applying a
spam detection tool (e-mails that do not pass this check are delivered to the
recipient, but are marked as spam and put in a special “spam” folder). It’s
intended that the system run on a single-core server machine (though it may
be moved to a multi-core server if the load gets too high).
You are in charge of deciding how the spam detection should be implemented.
A brief web search reveals that there are hundreds of existing software libraries
that can identify spam emails for you. They are written in a variety of different
languages and use a range of machine learning approaches. You could also
recommend a spam detector be developed in-hour.
What factors would you consider in deciding how spam detection would be
implement?
(Partially) document your design rationale. If you happen to be familiar with
any existing spam detection programs, you can use your knowledge of those.
But if not, see what information you can find out about existing programs from
a brief web search. (For fuller documentation of your design decisions, you’d
need to investigate those programs in more detail; but for the purposes of this
exercise, the information you find out from a web search will be enough.)
Your answer should clearly identify: the issue(s) being addressed, several
alternatives/proposals, criteria being used, any justifications, and a (tentative)
decision. Also mention any unresolved questions or assumptions you identify.

### Solution
**Issue:** Deciding between using existing spam filtering software or
developing a custom solution for the Email Filter system.

**Proposals**
P1: Use Existing Software: Integrate established spam filtering libraries.

**Arguments**
+ Quick Deployment: Integration with existing libraries can expedite the
implementation process.
+ Established Effectiveness: Many spam filtering libraries have been refined
over time and may offer high accuracy rates.
+ Low Maintenance: Updates and maintenance are typically handled by the
library maintainers, reducing the burden on the Email Filter system's
developers.
- Limited Customization: While some parameters may be adjustable, the
level of customization may be restricted compared to a custom solution.
- Dependency: Reliance on external libraries may introduce dependencies
and potential compatibility issues.
P2: Develop Custom Solution: Build a tailored spam filtering algorithm.
Arguments
+ Tailored Accuracy: A custom solution can be fine-tuned to the specific
characteristics of the Email Filter system, potentially leading to better
accuracy.
+ Performance Optimization: Optimization for the system's hardware and
workload could lead to improved performance.
+ Flexibility: Complete control over the algorithm allows for tailored
adjustments and enhancements as needed.
- Development Time: Building a custom solution requires time and resources
for design, implementation, and testing.
- Maintenance Overhead: Maintenance may require more effort initially, as
the system developers are responsible for updates and enhancements.

**Criteria:** performance optimization

**Resolution:** Choose based on project priorities, considering speed of
deployment, long-term effectiveness, and available resources. In this
content, resolution would be the custom solution.

## Question 2
For each of the following systems, discuss what type of software architecture
would be appropriate. Explain your reasoning. (A list of several architectures
we have looked at is supplied below, for your reference.)

1. Embedded software for an insulin pump. The system monitors a diabetic
patient’s blood sugar levels and their rate of change. If necessary, it
injects insulin (to mimic the normal function of the pancreas). If incorrect amounts are injected, a patient may go into a diabetic coma and
die. Medical products like this are heavily governed by legislation and
regulations.
2. A website for a graphic design business. The business owner wants to
make it easy for customers to upload existing artwork (logos, designs, etc)
and specifications, and download finished artwork. Customers should be
able to log onto the system to upload or download files.

### Solution
**1) Controller and process architecture：**

Controller components (subsystems):
- The controller component is responsible for making decisions and issuing
commands to regulate the insulin delivery process based on feedback from
sensors and higher-level control layers.
- It receives input from sensors monitoring the patient's blood sugar levels and rate of change, processes this information, and calculates the
appropriate insulin dosage.
- It interfaces with actuators to adjust insulin infusion rates and ensure precise control over insulin delivery.

Process components (subsystems):
- The process component represents the physiological process being controlled, which in this case is the regulation of blood sugar levels in a diabetic patient through insulin infusion.
- It involves the interaction between the insulin pump system and the patient's body, where insulin is delivered to mimic the function of the pancreas in response to changes in blood sugar levels.
- The goal of the process component is to maintain blood sugar levels within a target range while minimizing the risk of hypo- or hyperglycemia and ensuring patient safety.

**2）Client-Server Architecture:**
In this architecture, the system is divided into **two main components**: the
client side and the server side. The client side, typically a web browser or a
mobile app, interacts with the user and sends requests to the server. The
server side handles requests from clients, processes them, interacts with
databases or other external services, and sends back responses to clients.

Advantages:
- Simplicity: Client-server architecture is straightforward to implement and understand.
- Scalability: It allows for scaling the server side to handle increased traffic or workload.
- Separation of Concerns: The client and server components are logically separated, making it easier to maintain and update the system.

It could be some other architectures too as long as you can justify and briefly list the components (or subsystems) and how do they communicate and their responsibilities.
