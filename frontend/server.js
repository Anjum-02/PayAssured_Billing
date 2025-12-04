const express = require('express');
const fetch = require('node-fetch');
const bodyParser = require('body-parser');
const app = express();
const BACKEND = process.env.BACKEND_URL || 'http://127.0.0.1:8000';
app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));
app.get('/', async (req, res) => {
    const resp = await fetch(`${BACKEND}/cases`);
    const cases = await resp.json();
    const cre = await fetch(`${BACKEND}/clients`);
    const clients = await cre.json();
    const clientsMap = {}; clients.forEach(c=>clientsMap[c.id]=c.client_name);
    res.render('cases',{cases,clientsMap});
});
app.get('/cases/new', async (req, res) => {
    const resp = await fetch(`${BACKEND}/clients`);
    const clients = await resp.json();
    res.render('create_case',{clients});
});
app.post('/cases', async (req, res) => {
    const payload = {
        client_id: parseInt(req.body.client_id),
        invoice_number: req.body.invoice_number,
        invoice_amount: parseFloat(req.body.invoice_amount),
        invoice_date: req.body.invoice_date,
        due_date: req.body.due_date,
        status: req.body.status,
        last_follow_up_notes: req.body.last_follow_up_notes
    };
    await fetch(`${BACKEND}/cases`, {method:'POST', body: JSON.stringify(payload), headers:{'Content-Type':'application/json'}});
    res.redirect('/');
});
app.get('/cases/:id', async (req, res) => {
    const id = req.params.id;
    const resp = await fetch(`${BACKEND}/cases/${id}`);
    const data = await resp.json();
    const cre = await fetch(`${BACKEND}/clients`);
    const clients = await cre.json();
    const client = clients.find(c=>c.id===data.client_id) || {};
    res.render('case_detail',{caseItem:data, client});
});
app.post('/cases/:id/patch', async (req, res) => {
    const id = req.params.id;
    const payload = {status: req.body.status, last_follow_up_notes: req.body.last_follow_up_notes};
    await fetch(`${BACKEND}/cases/${id}`, {method:'PATCH', body: JSON.stringify(payload), headers:{'Content-Type':'application/json'}});
    res.redirect('/cases/' + id);
});
app.listen(3000, ()=>console.log('Frontend running on http://localhost:3000'));
