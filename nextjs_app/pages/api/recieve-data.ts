import type { NextApiRequest, NextApiResponse } from 'next'
import fs from 'fs';
import path from 'path';

// file path for data
const dataFilePath = path.resolve(__dirname, '../../../../data/data.json');

/**
 * Handles HTTP requests for storing and retrieving data.
 *
 * @param {NextApiRequest} req - incoming request object.
 * @param {NextApiResponse} res - outgoing response object.
 */
export default (req: NextApiRequest, res: NextApiResponse) => {
  if (req.method === 'POST') {
    try {
      let jsonData = req.body;

      if (jsonData === "No Solution") {
        jsonData = [{"Solution": false}];
      }

     else if (Object.keys(jsonData).length === 0 && jsonData.constructor === Object) {
        jsonData = [];
      }
      fs.writeFileSync(dataFilePath, JSON.stringify(jsonData, null, 2));

      res.status(201).json({ message: 'Data stored successfully' });


    } catch (error) {
      res.status(500).json({ message: 'Internal Server Error', error: error.message });
    }
  } 
  else if (req.method === 'GET') {
    try {
      const rawData = fs.readFileSync(dataFilePath, 'utf8');
      const data = JSON.parse(rawData);

      res.status(200).json(data);
    } catch (error) {
      res.status(500).json({ message: 'Internal Server Error', error: error.message });
    }
  } else {
    res.status(405).end();
  }
};