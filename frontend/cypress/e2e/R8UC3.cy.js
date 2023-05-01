// Preconditions
// The user is authenticated, has at least one task with at least one todo item associated to his account, and views this task in detail view mode.

// Main Success Scenario
// 1. If user clicks on the x symbol behind the description of the todo item, the todo item is deleted End Condition The todo item is removed from the todo list.

// Alternative Scenarios
// None

import "./login.cy"; // Logging in top the system

import "./R8UC1.cy"; // Create backlogs (backlog 1, backlog 2)

describe("R8UC3", () => {
    beforeEach(function () { // After each test
      cy.visit("http://localhost:3000/"); // Visit localhost
      cy.viewport(1920, 1080); // Set the viewport to 1920 x 1080
      cy.contains("div", "Email Address") // Look if the div contains email address
        .find("input[type=text]") // If true then find the text input
        .type("mon.doe@gmail.com"); // Enter the mail kappo1@gmail.com in the text input
  
      cy.get("form").submit(); // Submit the login form
      cy.get(".container-element a").last().click();
    });
  
    it("Main Success Scenario: Test to delete backlog 2 (The last todo-item)", () => {
      cy.get("li.todo-item").last().within(() => {
        cy.get("span").last().click();
      })
    });
  
    it("Main Success Scenario: Test to see if the backlog 2 is removed (The last todo-item)", () => {
        cy.get("li.todo-item").last().contains("span", "Backlog 2").should("not.exist");
    })
  });
