// Preconditions
// The user is authenticated, has at least one task with at least one todo item 
// associated to his account, and views this task in detail view mode.

// Main Success Scenario
// 1. The user clicks on the icon in front of the description of the todo item.
// 2. If the todo item was previously active, it is set to done.

// End Condition
// The toggled todo item is struck through. 

// Alternative Scenarios
// 2.b If the todo item was previously done, it is set to active. The toggled todo item is not struck through anymore.

import "./login.cy";

import "./R8UC1.cy";

describe("R8UC2", () => {
  beforeEach(function () { // After each test
    cy.visit("http://localhost:3000/"); // Visit localhost
    cy.viewport(1920, 1080); // Set the viewport to 1920 x 1080
    cy.contains("div", "Email Address") // Look if the div contains email address
      .find("input[type=text]") // If true then find the text input
      .type("mon.doe@gmail.com"); // Enter the mail kappo1@gmail.com in the text input

    cy.get("form").submit(); // Submit the login form
    cy.get(".container-element a").last().click();
  });

  it("Main Success Scenario: Test to click on the icon in front of the description of the todo item (When unchecked)", () => {
    cy.get("li.todo-item").last().within(() => {
      cy.get("span").first().click();
    })
  });

  it("Main Success Scenario: Test to see if the span is checked if it's set to done (active)", () => {
    cy.get("li.todo-item").last().within(() => {
      cy.get("span").first().get(".checked");
    })
  })

  it("Alternative Scenarios: Test to click on the icon in front of the description of the todo item (When checked)", () => {
    cy.get("li.todo-item").last().within(() => {
      cy.get("span").first().click();
    })
  });

  it("Alternative Scenarios: Test to see if the span is unchecked if it's set to undone (Not active)", () => {
    cy.get("li.todo-item").last().within(() => {
      cy.get("span").first().get(".unchecked");
    })
  });

});