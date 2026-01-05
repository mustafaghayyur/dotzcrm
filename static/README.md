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
This process assumes you have Node.js and npm installed. 

 1) Initialize your project: open your terminal and cd into current static folder:
  > npm init -y

  This creates a package.json file.

 2) Install development dependencies: Babel core, Webpack.
  > npm install --save-dev @babel/core @babel/cli @babel/preset-env webpack webpack-cli babel-loader

    - @babel/core is the main Babel functionality.
    - @babel/preset-env tells Babel which transformations and polyfills are needed based on your target environments.
    - babel-loader integrates Babel into Webpack.

 3) Configure Babel: create a configuration file (e.g., .babelrc or babel.config.json) in your project root to tell Babel to use the env preset:

    ```
    {
        "presets": ["@babel/preset-env"]
    }
    ```

 4) Configure Webpack: create a webpack.config.js file to define how your code should be processed and bundled:

    ```
    const path = require('path');

    const clientConfig = {
        entry: {
            core: './core/js/custom.js',
            tasks: './tasks/js/custom.js',
        }, // Your main ES6 entry files
        output: {
            filename: '[name].bundle.js', // The output ES5 bundle, [name] is replaced by the entry key
            path: path.resolve(__dirname, 'dist'),
        },
        module: {
            rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                loader: 'babel-loader',
                },
            },
            ],
        },
    };

    module.exports [clientConfig];
    ```

 5) Add a build script: in your package.json file, add a script to run Webpack:

    ```
    "scripts": {
        "build": "webpack"
    },
    ```

 6) Our JS source code will be found in the main_project_directory/static/ folder. In specfic, we have tried to organize all project-wide JS code under 'core' sub-folder; and app-specific libraries/code under the app's specific directory (i.e. static/tasks/ for example). 

 7) Compile your code. You can run the build script in your terminal:
  
  > npm run build

 This will create a dist/bundle.js file containing the ES5-compatible code. You can now open your index.html file in any browser, and it will run the compatible JavaScript. 