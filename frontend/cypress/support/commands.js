// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })

// yields elements with a data-test attribute that match a specified selector
Cypress.Commands.add("getBySel", (selector, ...args) => {
  return cy.get(`[data-test=${selector}]`, ...args)
})

// yields elements with a data-test attribute that contains a specified selector
Cypress.Commands.add("getBySelLike", (selector, ...args) => {
  return cy.get(`[data-test*=${selector}]`, ...args)
})

Cypress.Commands.add("login", (uid) => {
  cy.request(`http://localhost:5000/users/${uid}`).then((res) => {
    const user = res.body
    user.id = user._id.$oid
    delete user._id
    user.fullName = `${user.firstName} ${user.lastName}`

    cy.visit("/")
    cy.getBySel("email-input").type(user.email)
    cy.getBySel("login-submit").click()

    return cy.wrap(user)
  })
})
