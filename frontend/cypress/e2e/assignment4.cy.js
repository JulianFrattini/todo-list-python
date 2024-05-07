describe('Logging into the system', () => {
    // define variables that we need on multiple occasions
    let uid // user id
    let name // name of the user (firstName + ' ' + lastName)
    let email // email of the user
  
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

            console.log(response.body._id.$oid)

            let data = new FormData();
            data.append('title', 'task29292');
            data.append('description', '(add a description here)');
            data.append('userid', response.body._id.$oid);
            data.append('url', '');
            data.append('todos', ['Watch video']);
            cy.request({
                method: 'POST',
                url: 'http://localhost:5000/tasks/create',
                headers: {
                    'content-type': 'multipart/form-data',
                },
                body: data
            })
          })
        })
    })
  
    beforeEach(function () {
      cy.visit(`http://localhost:3000`)

      cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)


    // submit the form on this page
    cy.get('form')
      .submit()
    
    cy.contains('.title-overlay', 'task29292').click()
    })

    //
    // ID 1.1
    //
    it('new (active) todo item is appended to the bottom of the list of existing items', () => {
      // Add new todo item
      cy.get('input[placeholder*="Add a new todo item"]').type("next todo item")
      cy.contains('input', 'Add').click()
  
      cy.get('.todo-list').last().should('contain.text', 'next todo item')
      cy.contains('.todo-item', 'next todo item').find('span.remover').click()
    })

    //
    // ID 2.1
    //
    it('If the description is empty then the “Add” button should remain disabled', () => {
      cy.get('input[placeholder*="Add a new todo item"]')
      cy.contains('input', 'Add').should('be.disabled')
    })

    //
    // ID 2.2
    //
    it('the system creates a new todo item when description is not empty', () => {
      cy.get('input[placeholder*="Add a new todo item"]').type("next todo")
      cy.contains('input', 'Add').click()
      cy.get(".todo-item").should('contain.text', 'next todo')
      cy.contains('.todo-item', 'next todo').find('span.remover').click()
    })

    //
    // ID 3.1a
    //
    it ('when the user clicks on icon of an active todo item, it is set to done', () => {
      // Task should have todo item
      cy.contains('.todo-item', 'Watch video').find('span.checker').click()

      // See that circle is set to done, meaning class checker-checked 
      cy.contains('.todo-item', 'Watch video').find('span').should('has.class', 'checker checked')

      // Reset todo item to its original state
      cy.contains('.todo-item', 'Watch video').find('span.checker').click()
    })

    //
    // ID 3.1b
    //
    it ('when the user clicks on icon of an active todo item, it is struck through', () => {
      // Task should have todo item
      cy.contains('.todo-item', 'Watch video').find('span.checker').click()

      // See that when circle is set to done, description text is line-through
      cy.contains('.todo-item', 'Watch video').find('span.editable').invoke('css', 'text-decoration').should('contain', 'line-through')

      // Reset todo item to its original state
      cy.contains('.todo-item', 'Watch video').find('span.checker').click()
    })

    //
    // ID 3.2a
    //
    it ('when the user clicks on icon of a done todo item, it is set to active', () => {
      // Click on todo to make it done
      cy.contains('.todo-item', 'Watch video').find('span.checker').click()

      // Click on todo once more to make it active again
      cy.contains('.todo-item', 'Watch video').find('span.checker').click()

      // See that the done symbol is reverted back to a cirle
      cy.contains('.todo-item', 'Watch video').find('span').should('have.class', 'checker unchecked')
    })
    

    //
    // ID 3.2b
    //
    it ('when the user clicks on icon of a done todo item, it is not struck through', () => {
      // Click on todo to make it done
    cy.contains('.todo-item', 'Watch video').find('span.checker').click()

    // Click on todo to make it active again
    cy.contains('.todo-item', 'Watch video').find('span.checker').click()

    // See that when done symbol is reverted back to a cirle, the text is no longer line-through
    cy.contains('.todo-item', 'Watch video').find('span.editable').invoke('css', 'text-decoration').should('contain', 'solid')
    })

    //
    // ID 4.1
    //
    it ('when x symbol is pressed, todo item is deleted from the todo-list', () => {
      // Create a new todo item
      cy.get('input[placeholder*="Add a new todo item"]').type("final todo")
      cy.contains('input', 'Add').click()

      // Delete todo item
      cy.contains('.todo-item', 'final todo').find('span.remover').click()

      // Check deleted todo item is not in todo-list
      cy.get('.todo-list').should('not.include.text', 'final todo')
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