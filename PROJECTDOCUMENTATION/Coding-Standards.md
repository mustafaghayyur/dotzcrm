# Coding Standards

In this section we will outlines methodologies we employ for coding.

## Naming conventions:

#### Python/Backend Coding
We employ camel-case naming standards. Unfortunately due to Django's snake-case conventions, some elements sneak in snake-casing, however we are strictly trying to convert everything to Camel-case as we review code.

As such, all classes should start with a capital letter, and camel-cased the remainder of the name.

All functions/methods and variables should start with a lowercase first letter, and camel-cased the remainder of adjoined words.

#### Front-end Coding
All JS code should follow similar camel-case styling for 'classes' (read functions that follow a constructor approach and are located inside static/{app}/js/lib directory).

Methods and regular functions starting with a lower case first letter, with camlCasing the remaning adjoining words.


#### HTML DOM Markup in templates/
HTML (CSS) classes follow Bootstrap standard words-seperated-by-comma naming conventions. While IDs follow camel-casing with first letter (generally) being lower-case.


## Use of dictionaries over objects
In Python we tend to prefer dictionaries over objects, despite their crude look, so when handling complex data you should prefer dictionaries over objects.

However, when chosing to use objects to store complex data, our core.lib.state.EmptyObject should suffice as a neat object constructor for forming any data-object.

## Use of State() for data handling between classes of a module
We have employed core.lib.state.State() as a standard for all memory handling of complex modules thus far. We do not bar the use of custom attributes for classes you may design, however State() allows for increased use of Static classes. 

Since the master class of a module can define one state instance and pass it to static methods for various classes, design of complex logic becomes easier.

## In-code Documentation
We are constantly attempting to place insightful commentary for our code. Thus each method should contain the multi-line comment defining a concise explaination of said method, with appropriate param definitions to allow future developers a quick reference to your code.

"""
    It is our practice to indent all class-level and method level comments by one tab, for a clean visual effect. (like this line.)
"""

All paarms should ideally indicate what data types they should be with '|' pipe sepertion.

The 'returns' definition can also be defined, though we ahve yet to reach the level of organization to enforce those standard for all our code. Simply ensuring param-definitions in code-comments is sufficient.

## The 4-space-tab
All code should be edited with an editor configured to a 4-spaced tab rather than the standard \t space.

## Objects over helper functions
Helper functions found in core.helpers were instroduce early on, and can still be developed further when needed. They look visually satisfying and achieve most objectives.

However, we are more inclined to class-based code. All new code should attempt to find a class-based approach to solve problems. This will be desired.

## Where to place documentation
All documentation should ideally be organized in this directory 'PROJECTDOCUMENTATION'. In module-directory/README.md files are also fine for initial stages, though proper documentation should be added to PROJECTDOCUMENTATION/ at some point.


## Notes about our front-end JS stack

 - The JS $A library was born out of necessity when we decided or discovered our SPA oriented UX development. Ideally we would have chosen ReactJS for the SPA development, however our $A lib is unique in that it supports Bootstrap interactions, and is largely focussed on DOM manipulation.

 - We keep simple functions that are called recurringly in the core/js/helpers/ directory. Defining them in an appropriate exported objection as a callable property.

 - For more complex libraries that provide a more complete solution, such as the TabbedDashboard library, we define such constructor functions in the core/js/lib directory of static.

 - All our apps start with static/{app}/js/main.js file. Over here we begin a 'Main' program, that executes necessary unerlying operations to allow for speady development.
 
 - Our $A.query() library is central to the Universal API CRUD and List views. You are free to read through the $A.query() library in static/core/js/lib/query.js

