describe('Requirement 8: To-Do Item Management (R8UC1, R8UC2, R8UC3)', () => {
  
beforeEach(() => {
    // Load both fixtures
    cy.fixture('user.json').as('userData');
    cy.fixture('task.json').as('testTask');
    
    cy.visit('/'); 

    // Use the alias 'userData' to get the email from your JSON file
    cy.get('@userData').then((user) => {
      cy.get('input[name="email"]').type(user.email); // Types "mon.doe@gmail.com"
    });

    // Type your password (standard for this lab is usually '1234' or 'password')
    cy.get('input[type="submit"]').click({ force: true });
  });
  
  it('should create a new to-do item (R8UC1)', function() {
    // Revert to the selectors that worked previously
    cy.get('input[placeholder*="Add"]').type(this.testTask.todos, { force: true });
    cy.get('input[type="submit"]').contains('Add').click({ force: true }); 
    cy.contains(this.testTask.todos).should('be.visible');
  });

  it('should toggle a to-do item status (R8UC2)', function() {
    cy.contains(this.testTask.todos)
      .parent()
      .find('.checker, .toggle, [type="checkbox"], svg')
      .first()
      .click({ force: true });
    
    cy.contains(this.testTask.todos).should('have.css', 'text-decoration').and('match', /line-through/);
  });

  it('should delete a to-do item (R8UC3)', function() {
    cy.contains(this.testTask.todos)
      .parent()
      .find('.remover, .delete-icon, .remove-todo, .x-mark')
      .first()
      .click({ force: true });

    cy.contains(this.testTask.todos).should('not.exist');
  });
});