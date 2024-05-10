const backend_url = `http://localhost:5000`

describe('Todo', () => {
    let uid
    let email

    beforeEach(function () {
        // create a fabricated user from a fixture then create task and after that create todo
        cy.fixture('user.json')
        .then((user) => {
            cy.request({
                method: 'POST',
                url: `http://localhost:5000/users/create`,
                form: true,
                body: user
            })
            .then((response) => {
                uid = response.body._id.$oid
                email = user.email
              })
              .then(() => {
                cy.request({
                    method: 'POST',
                    url: `http://localhost:5000/tasks/create`,
                    form: true,
                    body: {
                    'title': "Test task",
                    'description': "Test description",
                    'userid': uid,
                    'url': 'someurl',
                    'todos': "Test todo"
                    }
                })
                .then(() => {
                    cy.visit('http://localhost:3000/')
                    cy.contains('div', 'Email Address')
                        .find('input[type=text]')
                        .type(email)
                    cy.get('form')
                    .submit()            
                    cy.get('.inputwrapper #title')
                        .type("Test title")
                    cy.get('.inputwrapper #url')
                        .type("LB8KwiiUGy0")
                    cy.get('form')
                        .submit()
            
                    cy.contains('Test title')
                        .click()
                    cy.get('.inline-form')
                        .type("Test todo item")
                        .submit()
                })
            })
        })
    })


    it('This test tests if beforeEach function creates user along with task and todo', () => {
      cy.contains('.todo-item', 'Test todo item');
    });

    it('R8UC1 - Creates a new todo and it appears last on the list', () => {
        cy.get('.todo-list')
            .find('.inline-form input[type="text"]')
            .type("This is another task", {force: true})
            .get('.inline-form input[value="Add"]')
            .click({force: true})
            .get('.todo-list')
            .find('.todo-item').last()
            .find('.editable')
            .should('have.text', "This is another task")
    });

    it('R8UC1 - Add button remains disabled for no description', () => {
      cy.get('.todo-list')
          .find('.inline-form input[type="text"]')
          .clear({force: true});
  
      cy.get('.todo-list')
          .find('.inline-form input[value="Add"]')
          .should('be.disabled');
    });
  
    it('R8UC1 - Add button does not remain disabled for a description', () => {
        cy.get('.todo-list')
            .find('.inline-form input[type="text"]')
            .type("This is another task", {force: true})
            .get('.inline-form input[value="Add"]')
            .should('not.be.disabled');
    });

    it('R8UC2 - The todo is struck through when the icon infront of Active item is clicked on, and the icon turns into a check mark.', () => {
        cy.contains('Test todo item')
            .get('.checker')
            .click({ multiple: true });
            
        cy.contains('.todo-item', 'Test todo item')
            .find('.checker', '.unchecked')
            .click({force: true})
            .parents('.todo-item')
            .find('.editable')
            .should('have.css', 'text-decoration-line', 'line-through');

        cy.get('.checker')
            .should('have.class', 'checked');
    });

    it('R8UC2 - The todo is not strikethrough when the icon in front of Done item is clicked on, and the check mark turns into a checker.', () => {
        cy.contains('Test todo item')
            .get('.checker')
            .click({ multiple: true });
    
        cy.contains('.todo-item', 'Test todo item')
            .find('.checker.unchecked')
            .click({ force: true });
    
        cy.contains('.todo-item', 'Test todo item')
            .find('.checker.checked')
            .click({ force: true })
            .parents('.todo-item')
            .find('.editable')
            .should('not.have.css', 'text-decoration-line', 'line-through');

        cy.get('.checker')
            .should('have.class', 'unchecked');
    });

    it('R8UC3 - Task should be removed from the list if X symbol behind a task is clicked on', () => {
        cy.intercept('DELETE', `**/todos/byid/*`).as('delTodo');

        cy.contains('.todo-item .editable', "Test todo")
            .parents('.todo-item')
            .find('.remover')
            .click({ force: true });

        cy.wait('@delTodo').then(() => {
           cy.wait(50000).contains('.todo-item .editable', "Test todo").should('not.exist')
        });
    });

    afterEach(function () {
        // clean up the database
        cy.request({
            method: 'DELETE',
            url: `${backend_url}/users/${uid}`
        });
    });
})
