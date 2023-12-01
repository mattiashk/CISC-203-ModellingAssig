import type { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';

const dataFilePath = path.resolve(__dirname, '../../../../data/data.json');

export default (req: NextApiRequest, res: NextApiResponse) => {
  try {
    const rawData = fs.readFileSync(dataFilePath, 'utf8');
    const data = JSON.parse(rawData);

    const { studentId, term } = req.query; // Get query parameters

    if (studentId && term) {
      // Find the specific student and term
      const studentData = data.find(student => student.student === studentId);
      const termData = studentData?.terms.find(t => t.term === mapTerm(term as string));
      if (!termData) {
        res.status(404).json({ message: 'Student or term not found' });
        return;
      }
      res.status(200).json(termData);
    } else {
      res.status(200).json(data);
    }
  } catch (error) {
    res.status(500).json({ message: 'Internal Server Error', error: error.message });
  }
};

function mapTerm(shortTerm: string): string {
  const termMap = { 'f': 'FALL', 'w': 'WINTER', 's': 'SUMMER' };
  return termMap[shortTerm.toLowerCase()] || '';
}
