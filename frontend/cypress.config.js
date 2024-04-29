const { defineConfig } = require("cypress")

module.exports = defineConfig({
  component: {
    devServer: {
      framework: "create-react-app",
      bundler: "webpack",
    },
  },
  e2e: {
    baseUrl: "http://localhost:3000",
    specPattern: "cypress/**/*.cy.{js,jsx,ts,tsx}",
    supportFile: "cypress/support/e2e.js",
    viewportHeight: 1000,
    viewportWidth: 1280,
    experimentalRunAllSpecs: true,
    setupNodeEvents(on, config) {
      on("task", {
        async "db:seed"() {
          const res = await fetch("http://localhost:5000/seed", {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
          });
          const uid = await res.json();
          return uid;
        },
      })

      return config
    },
  },
})
