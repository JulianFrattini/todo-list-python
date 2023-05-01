// Main Success Scenario
// 1. The user enters a description of a todo item into an empty input form field.
// 2. If the description is not empty and the user presses “Add”, the system creates a new todo item

// End Condition
// The new (active) todo item with the given description is appended to the bottom of the list of existing todo items.

// Alternative Scenarios
// 2.b If the description is empty then the “Add” button should remain disabled.
// describe("R8UC1", () => {
//   before(function () {
//     cy.visit("http://localhost:3000/users/create"); 
//   });

//   it("should create a new user", function () {
//     cy.request({
//       method: "POST",
//       url: "http://localhost:5000/users/create",
//       form: true,
//       body: {
//         email: "kappo3@gmail.com",
//         firstName: "kapp2",
//         lastName: "test",
//       },
//     }).then((response) => {
//       expect(response.status).to.eq(200); 
//     });
//   });


//   beforeEach(function () {
//     cy.visit("http://localhost:3000/");
//     cy.viewport(1920, 1080);
//     cy.contains("div", "Email Address")
//       .find("input[type=text]")
//       .type("kappo3@gmail.com");

//     cy.get("form").submit();
//   }); <-- om det skulle behövas, det med att skapa konton


describe("R8UC1", () => {
  beforeEach(function () { // After each test
    cy.visit("http://localhost:3000/"); // Visit localhost
    cy.viewport(1920, 1080); // Set the viewport to 1920 x 1080
    cy.contains("div", "Email Address") // Look if the div contains email address
      .find("input[type=text]") // If true then find the text input
      .type("mon.doe@gmail.com"); // Enter the mail mon.doe@gmail.com in the text input

    cy.get("form").submit(); // Submit the login form
  });

  it("Test create a task", () => {
    cy.contains("div", "Title").find("input[type=text]").type("Test task"); // Look if div contains Title then find the input text and write "Test task" in the input text
    cy.contains("Create new Task").click(); // Find the input "create new task" and click on it to create new task
  });

  it("Test if the task has been created", () => {
    cy.get(".container-element").contains("div", "Test task"); // FInd .cotainer-element and if it contains a div with a title of "Test task"
  });

  it("Test to open the task", () => {
    cy.get(".container-element a").last().click(); // Find the div with title Test task
    cy.get(".popup-inner").within(() => { // Get .popup-inner (the task popup)
      cy.contains("h1", "Test task"); // Within the .popup-inner find tag h1 with value "Test task"
    });
  });

  it("Test add 2 todo items", () => {
    cy.get(".container-element a").last().click(); // Find the div with title Test task

    // Create the first todo item
    cy.get(".inline-form").within(() => { // Get .inline-form (the todo item form)
      cy.get("input[type=text]").type("Backlog 1"); // Within the .inline-form get text input and type "Backlog 1"
      cy.get("input[type=submit]").click(); // Within the .inline-form get submit input and click on it to create a todo item in the task
    });

    // Create the second todo item
    cy.get(".inline-form").within(() => { // Get .inline-form (the todo item form)
      cy.get("input[type=text]").type("Backlog 2"); // Within the .inline-form get text input and type "Backlog 2"
      cy.get("input[type=submit]").click(); // Within the .inline-form get submit input and click on it to create a todo item in the task
    });
  });

  it("End Condition: Test if the new (active) todo item with the given description is appended to the bottom of the list of existing todo items ", () => {
    cy.get(".container-element a").last().click(); // Find the div with title Test task
    cy.get("li.todo-item").last().contains("span", "Backlog 2"); // Get the last li.todo-item in the todo-list and check if the span has title Backlog 2
  });

  it("Alternative Scenario: Test if add input is disabled if description is empty in the todo form", () => {
    cy.get(".container-element a").last().click(); // Find the div with title Test task
    cy.get(".inline-form").within(() => { // Get .inline-form (the todo item form)
      cy.get("input[type=submit]").should("be.disabled"); // Within the .inline-form get submit input and check if it's disabled (can not click on)
    });
  });
});
