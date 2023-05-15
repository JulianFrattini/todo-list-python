describe('GUI Testing', () => {
  let email;
  let userId;
  const taskName = 'testTask';
  const todoName = 'testTodo';
  const doneTodo = 'doneTodo';
  const notDoneTodo = 'notDoneTodo';
  const deleteTodo = 'deleteTodo';

  before(() => {
    cy.fixture('user.json').then(user => {
      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        form: true,
        body: user,
      }).then(response => {
        cy.visit('http://localhost:3000/').then(() => {
          email = response.body.email;
          userId = response.body._id.$oid;
          cy.get('#email').type(response.body.email).then(() => {
            cy.get('input[type="submit"]').click().then(() => {
              cy.get('#title').type(taskName).then(() => {
                cy.get('form').submit().then(() => {
                  cy.contains('div', taskName).click().then(() => {
                    cy.get('.inline-form').type(doneTodo).then(() => {
                      cy.get('.inline-form').submit().then(() => {
                        cy.get('.inline-form').type(deleteTodo).then(() => {
                          cy.get('.inline-form').submit().then(() => {
                            cy.get('.inline-form').type(notDoneTodo).then(() => {
                              cy.get('.inline-form').submit().then(() => {
                            cy.request({
                              method: 'GET',
                              url: `http://localhost:5000/tasks/ofuser/${userId}`,
                            }).then((response) => {
                              const todoId = response.body[0].todos[1]._id.$oid;
                                const data = new URLSearchParams();
                                data.append('data', `{'$set': {'done': true}}`);
                                fetch(`http://localhost:5000/todos/byid/${todoId}`, {
                                    method: 'put',
                                    body: data,
                                    headers: { 'Cache-Control': 'no-cache' }
                                })
                            });
                          });
                        });
                      });
                    });
                  });
                });
                  });
                });
              });
            });
          });
        });
      });
    });
  });
  
  
  

  beforeEach(() => {
    cy.visit('http://localhost:3000/')
    cy.get('#email').type(email)
    cy.get('input[type="submit"]').click()
    cy.contains('div', taskName).click()

  })

  // R8UC1 - Test case 1
  it(' Add a valid todo item', () => {
    cy.get(".inline-form").type(todoName)
    cy.get(".inline-form").submit()
    cy.get('.todo-item .editable')
      .contains(todoName)
      .should('exist')

  })
  // R8UC1 - Test case 2
  it('Add an empty todo item', () => {
    cy.get('.inline-form input[type="submit"]')
      .should('be.disabled'); // check if the submit button is initially disabled
    cy.get('.inline-form input[type="submit"]').click({ force: true }); // try click the button anyways
    cy.get('.todo-item .editable')
      .should('have.length', 5); //check that no extra todos have been added

    // cy.get(".inline-form").submit()
    // cy.get('.todo-item .editable')
    // .should('have.length', 2); //check that no extra todos have been added (in this case length = 3, because we bypass the disable property on the button)
  });

  // R8UC2 - Test case 1
  it('Toggle an active todo item to done', () => {

    cy.contains('.editable', notDoneTodo)
      .parent('.todo-item')
      .find('span.checker') // find the span.checker element within the .todo-item element
      .click({ force: true })
      .wait(1500)
      .should('have.class', 'checked');

    cy.contains('.editable', notDoneTodo)
      .parent('.todo-item')
      .find('span.editable') // find the span.checker element within the .todo-item element
      .should('have.css', 'text-decoration')
      .and('match', /line-through/);

  })

  // R8UC2 - Test case 2
  it('Toggle a done todo item to active', () => {
    cy.contains('.editable', doneTodo)
      .parent('.todo-item')
      .find('span.checker')
      .click({ force: true })
      .wait(1500)
      .should('have.class', 'unchecked');

    cy.contains('.editable', doneTodo)
      .parent('.todo-item')
      .find('span.editable')
      .should('have.css', 'text-decoration')
      .and('not.match', /line-through/);
  })

  // R8UC3 - Test case 1
  it('Delete an Todo item', () => {

    cy.get('.todo-item .editable')
    .should('have.length', 5); //check that length is 2 before deletion

    cy.contains('.editable', deleteTodo)
      .parent('.todo-item')
      .find('span.remover')
      .click({ force: true })

    cy.contains('.editable', deleteTodo)
    .should('not.exist')

    cy.get('.todo-item .editable')
    .should('have.length', 4); //check that the todo have been deleted

  })


  after(async () => {
    const response = await fetch(`http://localhost:5000/users/bymail/${email}`)
    const result = await response.json();
    const userId = result._id.$oid
    await cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${userId}`
    })
  })

})
