const { defineConfig } = require("cypress");

module.exports = defineConfig({
  viewportWidth: 1920,  // Set the desired width of the viewport
  viewportHeight: 1080,  // Set the desired height of the viewport
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
