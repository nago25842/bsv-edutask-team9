describe('Requirement 8: To-Do Item Management (R8UC1, R8UC2, R8UC3)', () => {
  
  beforeEach(() => {
    cy.fixture('user.json').as('userData');
    cy.fixture('task.json').as('testTask');
    cy.visit('/'); 

    cy.get('@userData').then((user) => {
      cy.get('input[name="email"]').type(user.email); 
    });
    cy.get('input[type="submit"]').first().click({ force: true });

    cy.get('body').then(($body) => {
      if ($body.text().includes('Top 7 Awesome Developer Tools')) {
        cy.contains('Top 7 Awesome Developer Tools').click();
      } else {
        cy.get('input[placeholder="Title of your Task"]').type('Top 7 Awesome Developer Tools');
        cy.get('input[placeholder*="Viewkey"]').type('dQw4w9WgXcQ'); 
        cy.get('input[type="submit"]').contains('Create new Task').click({ force: true });
        cy.contains('Top 7 Awesome Developer Tools').click();
      }
    });
  });

  after(() => {
    cy.fixture('user.json').then((user) => {
      if (user.id) {
        cy.request({ method: 'GET', url: `http://localhost:5000/tasks/ofuser/${user.id}`, failOnStatusCode: false })
          .then((response) => {
            if (response.body && Array.isArray(response.body)) {
               response.body.forEach(task => {
                 if (task.title === 'Top 7 Awesome Developer Tools' || task.title.includes('DeleteMe')) {
                   cy.request({ method: 'DELETE', url: `http://localhost:5000/tasks/${task._id}`, failOnStatusCode: false });
                 }
               });
            }
          });
      }
    });
  });

  it('TC1 - should create a new to-do item (R8UC1)', function () {
    cy.get('input[placeholder*="Add"]').type(this.testTask.todos, { force: true });
    cy.get('input[type="submit"]').contains('Add').click({ force: true }); 
    cy.contains(this.testTask.todos, { timeout: 10000 }).should('exist');
  });

  it('TC2 - should not create a to-do item with empty input (R8UC1)', function () {
    cy.get('input[placeholder*="Add"]').clear({ force: true });
    cy.get('input[type="submit"]').contains('Add').click({ force: true });
    cy.wait(1000); 
    // Assert that no list item contains an empty string (or empty content)
    cy.get('.todo-item').each(($el) => {
       cy.wrap($el).invoke('text').should('not.be.empty');
    });
  });

  it('TC3 - should mark a to-do item as done (R8UC2)', function () {
    cy.get('input[placeholder*="Add"]').type(this.testTask.todos, { force: true });
    cy.get('input[type="submit"]').contains('Add').click({ force: true });
    cy.contains(this.testTask.todos).scrollIntoView({ position: 'center' })
      .parent().find('.checker, .toggle, [type="checkbox"], svg').first().click({ force: true });
    cy.contains(this.testTask.todos).should('have.css', 'text-decoration').and('match', /line-through/);
  });

  it('TC4 - should mark a to-do item as active (R8UC2)', function () {
    cy.get('input[placeholder*="Add"]').type(this.testTask.todos, { force: true });
    cy.get('input[type="submit"]').contains('Add').click({ force: true });
    const todo = cy.contains(this.testTask.todos).scrollIntoView({ position: 'center' });
    todo.parent().find('.checker').first().click({ force: true });
    todo.parent().find('.checker').first().click({ force: true });
    cy.contains(this.testTask.todos).should('not.have.css', 'text-decoration', 'line-through');
  });

  it('TC5 - should delete a to-do item (R8UC3)', function () {
    const uniqueTodo = 'DeleteMe' + Date.now();
    cy.get('input[placeholder*="Add"]').type(uniqueTodo, { force: true });
    cy.get('input[type="submit"]').contains('Add').click({ force: true });
    cy.contains(uniqueTodo).scrollIntoView({ position: 'center' }).should('exist');
    cy.contains(uniqueTodo).parent().find('.remover, .delete-icon').first().click({ force: true });
    cy.reload();
    cy.contains(uniqueTodo).should('not.exist');
  });
});