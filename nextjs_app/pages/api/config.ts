import { NextApiRequest, NextApiResponse } from 'next';
import { loadConfig } from '../../utils/config';


export default function handler(req: NextApiRequest, res: NextApiResponse) {
    const config = loadConfig();
    res.status(200).json({
      web_app_port: config.web_app_port,
      sat_solver_port: config.sat_solver_port
    });
  }
