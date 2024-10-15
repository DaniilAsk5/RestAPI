document.addEventListener("DOMContentLoaded", function () {
  const itemList = document.getElementById("item-list");
  const itemForm = document.getElementById("item-form");

  async function fetchItems() {
    const response = await fetch('/items');
    const items = await response.json();
    itemList.innerHTML = '';
    items.forEach(item => {
      const li = document.createElement("li");
      li.textContent = `${item.name}: ${item.description}`;
      itemList.appendChild(li);
    });
  }

  itemForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const name = document.getElementById("name").value;
    const description = document.getElementById("description").value;

    const response = await fetch('/items', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name, description }),
    });

    if (response.ok) {
      const newItem = await response.json();
      fetchItems(); 
    }
  });

  fetchItems();
});