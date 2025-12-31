## Bootsrap Setup Instructions

We will be using Boostrap for all UI/UX development of Dotz CRM + PM Software.

See more at: https://getbootstrap.com/ 

While we may not do much in customization of vanilla bootstrap styles, you should download the the following via npm to do your own corporate assimilation:

1) in your terminal console, cd into this static directory.

2) run: npm install bootstrap@v5.3.8

3) Install a Sass compiler, like so:
 > npm install -g sass

4) Examine our Sass files found in static/scss/ directory. You can modify or add to, as you deem appropriate.

5) Once satisfied with your changes, you may compile the code:
 > sass ./scss/custom.scss:./css/custom.css --style=compressed
 (while cd'd in the static folder of this codebase.)

6) Run your application and refresh your front-end code to see your changes.

Also see Bootstrap's documentation on customizing Sass:
https://getbootstrap.com/docs/5.3/customize/sass/
