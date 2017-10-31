## Web Site Construction
In this part, we will construct a simple website in order to conduct a silly experiment. Construction of this simple website will introduce some fundamental concepts and give us something to use in later parts of the tutorial. Companion code for this part can be found in the directory `\website-tutorial-wrapper`. The companion code can be run directly from you local machine by opening `index.html` with your preferred browser. Right click `index.html`, select "open as...", and select a browser. In this part of the tutorial, the website will not be made publicly accessible.

### The Simple Experiment
In the web experiment, participants will be shown one of two letters (A or B). Upon seeing the letters, participants must click one of two buttons labeled "A" or "B". After responding, participants will receive feedback if they were correct. A working version of this experiment can be seen at [www.mozerlab.us/server-tutorial](https://www.mozerlab.us/server-tutorial).

### Three Conceptual Pieces
In order to construct this website, we will follow best practices and split the construction of the website into three different conceptual pieces: content, style, and behavior. We will place each conceptual piece in a separate file:
* Content - `index.html`
* Style - `general.css`
* Behavior - `AppController.js`

As you can see from the filename extensions, we will be using three different languages: HTML, CSS, and JavaScript.

Let's start with the content of the website. The `index.html` file specifies all of the web elements that we want to use in our experiment. Web elements include things like paragraphs, buttons, input boxes, and more abstract elements such as divs. When assembled correctly, a collection of web elements create a sensible website. If you are new to HTML, check out the in-depth HTML tutorial at w3schools (https://www.w3schools.com/html/). In the header, we import the files `general.css` and `AppController.js`. We also import the convenient jQuery and Bootstrap libraries ( 'jquery.js', 'bootstrap.js', and 'bootstrap.css'). To make the layout of the page neat and professional, we use Bootstrap's grid system (http://getbootstrap.com/docs/4.0/layout/grid/). All of the content related to the experiment will reside in three divs with the class `begin-content`, `trial-content`, and `end-content`. The experiment instructions are placed in `begin-content`, the trial content in `trial-content`, and the concluding instructions in `end-content`. The three most important elements are the stimulus (`id=trial-content__stimulus`) and the two submission buttons (`class=content__submit-button`). At the bottom of `index.html`, there is a block of JavaScript code that creates an `AppController` object *after* the page elements finish loading. We pass the `AppController` a configuration variable `cfg` that specifies the number of trials and whether we should print debug messages to the browser console.

The style (i.e., look) of the experiment is specified in our `general.css` file. To help keep the code legible, element IDs and classes are named using block, element, modifier (BEM) conventions (http://getbem.com/naming/). While any styling is possible, it is best to make the webpage look as clean and professional as possible.

The behavior of the experiment is governed by the code contained in the `AppController.js` file. Following common practice, we have wrapped most of the behavior code in a JavaScript object called `AppController` in order to limit the number of variables in the global namespace. Since this is a simple experiment, only a handful of functions are necessary to operate the entire website. In addition to `AppController.js`, we have a second JavaScript file called 'utils.js', which provides utility functions. At the moment, the only utility function we have is `Console_Debug` which prints out messages to the browser console if `cfg.debugOn` is true. We can use `Console_Debug` to help us diagnose issues during web development.

To keep our files nice and organized, we will be using the following file architecture:
* `\website-tutorial`
  * `index.html`
  * `\css`
    * `bootstrap.css`
    * `general.css`
  * `\js`
    * `AppController.js`
    * `bootstrap.js`
    * `jquery-1.11.3.js`
    * `jquery-ui-1.12.1.min.js`
    * `utils.js`

NOTE: In principle, we could also specify style and behavior in the `index.html` file, but best practice is to keep them separate.

### Additional Resources
More in-depth tutorials of each of the languages and libraries used in this part can be found at w3schools:
* HTML (https://www.w3schools.com/html/)
* CSS (https://www.w3schools.com/css/)
* JavaScript (https://www.w3schools.com/js/)
* jQuery (https://www.w3schools.com/jquery/)
* Bootstrap (https://www.w3schools.com/bootstrap/)
