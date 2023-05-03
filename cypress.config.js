const { defineConfig } = require("cypress");

module.exports = defineConfig({
  projectId: 'dyt27y',
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
