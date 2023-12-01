import type { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';

const dataFilePath = path.resolve(__dirname, '../../../../data/data.json');

export default (req: NextApiRequest, res: NextApiResponse) => {
  try {
    const rawData = fs.readFileSync(dataFilePath, 'utf8');
    const studentsData = JSON.parse(rawData);

    const overviewData = studentsData.map(student => {
      const terms = {
        Fall: student.terms.some(term => term.term === "FALL") ? true : false,
        Winter: student.terms.some(term => term.term === "WINTER") ? true : false,
        Summer: student.terms.some(term => term.term === "SUMMER") ? true : false,
      };

      return {
        Name: student.student,
        Fall: terms.Fall,
        Winter: terms.Winter,
        Summer: terms.Summer,
      };
    });

    res.status(200).json(overviewData);
  } catch (error) {
    res.status(500).json({ message: 'Internal Server Error', error: error.message });
  }
};
