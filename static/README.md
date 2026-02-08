# Bootsrap Setup Instructions

We will be using Boostrap for all UI/UX development of Dotz CRM + PM Software.

See more at: https://getbootstrap.com/ 

While we may not do much in customization of vanilla bootstrap styles, you should download the the following via npm to do your own corporate assimilation:

1) in your terminal console, cd into this static directory.

2) run: npm install bootstrap@v5.3.8

3) Install a Sass compiler, like so:
 > npm install -g sass

4) Examine our Sass files found in static/scss/ directory. You can modify or add to, as you deem appropriate.

5) Once satisfied with your changes, you may compile the code:

 > sass ./scss/dotzstrap.scss:./css/dotzstrap.css --style=compressed
 
 (while cd'd in the static folder of this codebase.)

6) Run your application and refresh your front-end code to see your changes.

Also see Bootstrap's documentation on customizing Sass:
https://getbootstrap.com/docs/5.3/customize/sass/


### Notes
 - To keep the custom.scss file auto-recompile mode, while testing, you can also run (in dev environment):

  > sass --watch ./scss/dotzstrap.scss ./css/dotzstrap.css

 View useable icons:
 https://icons.getbootstrap.com/




 # JS Code-base Development Evironment setup:
#### (following was taken from Google AI's anwers):

To run a web app using ES6 code across a wide range of browsers, you need to use a transpiler (like Babel or SWC) to convert your modern JavaScript into a backward-compatible version (typically ES5). This process is essential because older browsers may not support all ES6+ features. 

Here is a general guide on how to set up your workflow:
Key Tools Needed
 - Babel: The most widely used JavaScript transpiler for converting ES6+ syntax (like arrow functions, const/let, classes) into ES5.
 - A Module Bundler: Tools like Webpack, Rollup, or Parcel.
 - Polyfills: These are code snippets that provide the functionality for newer APIs (like Promise or Array.from) that Babel can't simply "transpile".


### Step-by-Step Setup using Babel and Webpack

In your commandline utility, cd into static/ directory.

run:
 > npm run build
Builds all jd bundle files: 
 - static/dist/users-bundle.js 
 - static/dist/tasks-bundle.js , etc...

