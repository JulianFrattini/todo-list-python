describe('Testing todo-items', () => {
    let uid;  // User ID
    let email;  // User's email
    let name;  // User's full name

    before(function () {
        // Create a user
        cy.fixture('user.json')
          .then((user) => {
            cy.request({
              method: 'POST',
              url: `http://localhost:5000/users/create`,
              form: true,
              body: user
            }).then((response) => {
              uid = response.body._id.$oid;
              name = `${user.firstName} ${user.lastName}`;
              email = user.email;
            });
          });
    });

    beforeEach(() => {
        cy.visit('http://localhost:3000');
        cy.contains('div', 'Email Address').find('input[type=text]').type(email);
        cy.get('form').submit();
        cy.get('h1').should('contain.text', `Your tasks, ${name}`);
        cy.get('#title').type('idrott');
        cy.get('#url').type('https://youtube.com/watch?v=XYZ');
        cy.get('form').submit();
        cy.get('.title-overlay').contains('idrott').click();
    });


    it('TC1: Valid input description of todo item', () => {
        cy.get('input[type="text"][placeholder="Add a new todo item"]').type('Finish idrott', { force: true });
        cy.get('input[type="submit"][value="Add"]').click({ force: true });
        cy.get('ul.todo-list li.todo-item span.editable').should('contain', 'Finish idrott');
    });

    it('TC2: Empty input description of todo item', () => {
        cy.get('input[type="submit"][value="Add"]').should('be.disabled');
    });

    it('TC3: Whitespace input', () => {
        cy.get('input[type="text"][placeholder="Add a new todo item"]').type('   ', { force: true });
        cy.get('input[type="submit"][value="Add"]').should('be.disabled');
    });

    it('TC4: Multiple rapid clicks to test duplicate handling', () => {
        const inputField = 'input[type="text"][placeholder="Add a new todo item"]';
        const addButton = 'input[type="submit"][value="Add"]';

        const addItem = (itemText) => {
            cy.get(inputField).clear({ force: true }).type(itemText, { force: true }); // Force clearing and typing
            cy.get(addButton).click({ force: true });
        };

        // Add the same 'Review video' item multiple times
        addItem('Review video');
        addItem('Review video');

        // Check that the text 'Review video' is present in at least one item
        cy.get('ul.todo-list li.todo-item span.editable').should('contain', 'Review video');

    });



    it('TC5: Mark todo item as “done”', () => {
        // Select the first todo item and click the checker span to mark it as done
        cy.get('ul.todo-list li.todo-item').first().find('span.checker').click();

        // Verify that the span now has the 'checked' class for the first item
        cy.get('ul.todo-list li.todo-item').first().find('span.checker').should('have.class', 'checked');
    });


    it('TC6: Change “done” item to “active” item', () => {
        // Click the checker span to toggle the state of the todo item to active (or unchecked)
        cy.get('ul.todo-list li.todo-item').first().find('span.checker').click();

        // Verify that the span no longer has the 'checked' class indicating it is no longer marked as done
        cy.get('ul.todo-list li.todo-item').first().find('span.checker').should('have.class', 'unchecked');
    });

    it('TC7: Toggle item repeatedly', () => {
        const toggleTimes = 3;  // Define how many times to toggle the item
        for (let i = 0; i < toggleTimes; i++) {
            // Click the checker span each time in the loop to toggle the todo item's state
            cy.get('ul.todo-list li.todo-item').first().find('span.checker').click();
        }

        // Determine the final expected state based on whether the number of toggles is odd or even
        // Odd number of toggles would leave the item in the "done" state (checked)
        if (toggleTimes % 2 === 1) {
            cy.get('ul.todo-list li.todo-item').first().find('span.checker').should('have.class', 'checked');
        } else {
            // Even number of toggles would revert it to the initial state (unchecked)
            cy.get('ul.todo-list li.todo-item').first().find('span.checker').should('not.have.class', 'checked');
        }
    });


    it('TC8: Delete to-do item from the list', () => {

        // Perform the deletion on the first todo item
        cy.get('ul.todo-list li.todo-item').first().find('span.remover').click();

    });


    it('TC9: Delete all to-do items in the list', () => {
        // First, ensure there are items to delete.
        cy.get('ul.todo-list li.todo-item').should('exist');

        // Then, click each delete button
        cy.get('ul.todo-list li.todo-item').each(($item) => {
            cy.wrap($item).find('span.remover').click();
        });

        // check that no todo items are left
        cy.get('ul.todo-list li.todo-item').should('not.exist');
    });

    afterEach(function () {
        // clean up by deleting the user from the database
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/todos/byid/${uid}`,
            failOnStatusCode: false
        }).then(response => {
            console.log('Deleted all tasks for user', response);
        });

    });

    after(function () {
        // clean up by deleting the user from the database
        cy.request({
          method: 'DELETE',
          url: `http://localhost:5000/users/${uid}`
        }).then((response) => {
          cy.log(response.body)
        })

    });

});
