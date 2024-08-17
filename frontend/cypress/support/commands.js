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

// commans for creating a user for login. 
Cypress.Commands.add('createUser', () => {
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
            cy.wrap(response.body._id.$oid).as('uId')
            cy.wrap(user.firstName + ' ' + user.lastName).as('userName')
            cy.wrap(user.email).as('userEmail')
        })
      })
  });


Cypress.Commands.add('login', (email) => {
    cy.visit('http://localhost:3000')
    cy.contains('div', 'Email Address').find('input[type=text]').type(email)
    cy.get('form').submit()
    cy.get('h1').should('contain.text', 'Your tasks')

})

Cypress.Commands.add('resettest', () => {
  cy.get('@uId').then((uId) => {
      cy.request({
          method: 'DELETE',
          url: `http://localhost:5000/users/${uId}`
      }).then(response => {
          cy.log(response.body)
      });
  });
});


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