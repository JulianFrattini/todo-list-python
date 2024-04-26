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
                // form: true,
                headers: {
                    'content-type': 'multipart/form-data',
                },
                body: data
            })
          })
        })
    })
  
    beforeEach(function () {
      // enter the  main page
      cy.visit('http://localhost:3000')
    })

    it('starting out on the landing screen', () => {
        // make sure the landing page contains a header with "login"
        cy.get('h1')
          .should('contain.text', 'Login')
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