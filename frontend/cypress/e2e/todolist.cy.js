import "./login.cy"; // Import the login functionality

// Test suite for creating to-do items
describe("R8UC1: Create To-Do Items", () => {
  // Log in and set up the initial state before the test suite
  before(() => {
    cy.visit("http://localhost:3000/");
    cy.viewport(1920, 1080);
    cy.contains("div", "Email Address")
      .find("input[type=text]")
      .type("mon.doe@gmail.com");

    cy.get("form").submit();
    cy.contains("div", "Title")
      .find("input[type=text]")
      .type("Test task");
    cy.contains("Create new Task").click();
  });

  // Log in before each test case
  beforeEach(() => {
    cy.visit("http://localhost:3000/");
    cy.viewport(1920, 1080);
    cy.contains("div", "Email Address")
      .find("input[type=text]")
      .type("mon.doe@gmail.com");

    cy.get("form").submit();
  });

  // Test case for adding two valid to-do items
  it("R8UC1_1 and R8UC1_2: Add two todo items with valid texts", () => {
    cy.get(".container-element a").last().click();

    // Create the first todo item
    cy.get(".inline-form").within(() => {
      cy.get("input[type=text]").type("Task 1");
      cy.get("input[type=submit]").click();
    });

    // Create the second todo item
    cy.get(".inline-form").within(() => {
      cy.get("input[type=text]").type("Task 2");
      cy.get("input[type=submit]").click();
    });
  });

  // Test case for verifying the new to-do item is added at the bottom of the list
  it("End Condition: Verify new todo item is added at the bottom of the list", () => {
    cy.get(".container-element a").last().click();
    cy.get("li.todo-item").last().contains("span", "Task 2");
  });

  // Test case for checking if the input is disabled with an empty description
  it("Alternative Scenario: Check if input is disabled with an empty description", () => {
    cy.get(".container-element a").last().click();
    cy.get(".inline-form").within(() => {
      cy.get("input[type=submit]").should("be.disabled");
    });
  });
});

// Test suite for toggling the completion status of a to-do item
describe("R8UC2: Toggle the completion status of a to-do item", () => {
  // Log in before each test case
  beforeEach(() => {
    cy.visit("http://localhost:3000/");
    cy.viewport(1920, 1080);
    cy.contains("div", "Email Address")
      .find("input[type=text]")
      .type("mon.doe@gmail.com");

    cy.get("form").submit();
    cy.get(".container-element a").last().click();
  });

  // Test case for toggling the status of an incomplete to-do item to complete
  it("R8UC2.1: Toggle the status of an incomplete to-do item to complete", () => {
    cy.get("li.todo-item").last().within(() => {
      cy.get("span").first().click(); // Click on the first span (when it's unchecked)
    });
  });

  it("R8UC2.2: Toggle the status of a completed to-do item to incomplete", () => {
    cy.get("li.todo-item").last().within(() => {
      cy.get("span").first().click(); // Click on the first span (when it's unchecked)
    });

    //Toggle the status back to incomplete
    cy.get("li.todo-item").last().within(() => {
      cy.get("span").first().click(); // Click on the first span (when it's checked)
    });

  });
});

// Test suite for deleting a to-do item
describe("R8UC3: Delete a to-do item", () => {
  // Log in before each test case
  beforeEach(() => {
    cy.visit("http://localhost:3000/");
    cy.viewport(1920, 1080);
    cy.contains("div", "Email Address")
      .find("input[type=text]")
      .type("mon.doe@gmail.com");

    cy.get("form").submit();
    cy.get(".container-element a").last().click();
  });

  // Test case for deleting the last to-do item
  it("R8UC3_1: Delete the last to-do item", () => {
    cy.get("li.todo-item").last().within(() => {
      cy.get("span").last().click(); // Assuming the last span is the delete button
    });
  });

  // Test case for verifying the last to-do item is removed
  it("R8UC3_2: Verify the last to-do item is removed", () => {
    cy.get("li.todo-item").last().contains("span", "Task 2").should("not.exist");
  });
});
