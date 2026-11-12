\# Security baseline – open recipe API



Date: 2026-11-12



\- Anonymous \*\*GET /recipes\*\*  

&#x20; - No auth headers sent.  

&#x20; - Response: 200 OK, full list of recipes with `id`, `title`, and `instructions`.  

&#x20; - Impact: Any anonymous caller can read all recipe data.



\- Anonymous \*\*POST /recipes\*\*  

&#x20; - No auth headers sent.  

&#x20; - Body: `{ "title": "Anon Test", "instructions": "Created without auth" }`  

&#x20; - Response: 201/200 OK with JSON for a new recipe (id 3).  

&#x20; - Follow‑up GET shows the new recipe in the list.  

&#x20; - Impact: Any anonymous caller can create new recipes and pollute the data.



\- Anonymous \*\*PATCH /recipes/3\*\*  

&#x20; - No auth headers sent.  

&#x20; - Body: `{ "title": "Anon Updated", "instructions": "Updated without auth" }`  

&#x20; - Response: 200 OK with updated JSON for recipe id 3.  

&#x20; - Follow‑up GET shows updated fields.  

&#x20; - Impact: Any anonymous caller can modify existing recipes.



\- Anonymous \*\*DELETE /recipes/3\*\*  

&#x20; - No auth headers sent.  

&#x20; - Response: 204 No Content (or 200 OK).  

&#x20; - Follow‑up GET /recipes shows id 3 is gone.  

&#x20; - Impact: Any anonymous caller can delete recipes permanently.



Summary:  

The API is \*\*functionally correct\*\* (returns expected data and status codes) but \*\*not secure\*\*. It does not perform any identity or permission checks; it trusts every caller. Anyone who can reach the URL can read, create, update, or delete recipes. Hiding the URL would not prevent abuse once it is discovered.

