let uid // user id
let name // name of the user (firstName + ' ' + lastName)
let email // email of the user
let counter = 1


describe('Logging into the system', () => {
  // define variables that we need on multiple occasions

  before(function () {
    // create a fabricated user from a fixture
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
          uid = response.body._id.$oid
          name = user.firstName + ' ' + user.lastName
          email = user.email
        })
      })
  })

  beforeEach(function () {
    // enter the main main page
    cy.visit('http://localhost:3000')

    // log in
    cy.get("#email")
      .type(email)
    cy.get(".submit-form input[type=submit]")
      .click()
  
    // make task
    cy.get("#title")
      .type("Task " + counter.toString())
      counter++
    cy.get(".submit-form input[type=submit]")
      .click()
  })

  it('Add todo to task1', () => {
    // open task
    cy.get(".container-element:nth-of-type(1) a").click();
    cy.get(".popup").contains("Task 1");
  
    // make sure you cant add empty todo
    cy.get(".inline-form input[type=submit]").should("be.disabled");
  
    // write todo text
    cy.get(".inline-form input[type=text]").type("My TODO item");
  
    // click add
    cy.get(".inline-form input[type=submit]").click();

    // make sure added TODO is last
    cy.get(".todo-list:last-of-type")
      .contains("My TODO item");
  })

  it("Check of todo item", () => {
    // open task
    cy.get(".container-element:nth-of-type(2) a")
      .click();
    cy.get(".popup")
      .contains("Task 2");

    cy.get(".todo-item:nth-of-type(1) .checker")
      .click()
      .get(".todo-item:nth-of-type(1) .unchecked")
  })

  it("Remove task", () => {
    cy.get(".container-element:nth-of-type(3) a")
      .click();
    cy.get(".popup")
      .contains("Task 3");

    // make sure 1 todo(+ form) exists
    cy.get(".todo-list")
      .children()
      .should("have.length", 2)

    // remove todo
    cy.get(".todo-item:nth-of-type(1) .remover")
      .contains("✖")
      .click()
      .click()
    
    // make sure 0 todos(+ form) exists
    cy.get(".todo-list")
      .children()
      .should("have.length", 1)
  })

  after(function () {
    // clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})