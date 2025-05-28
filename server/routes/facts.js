const express = require('express');
const router = express.Router();
const db = require('../db/connection');

router.get('/api/facts', async (req, res) => {
  try {
    const facts = await db.query('SELECT * FROM facts');
    res.json(facts.rows);
  } catch (error) {
    console.error('Database error:', error);
    res.status(500).json({ 
      error: 'Internal server error',
      details: error.message 
    });
  }
});

module.exports = router;