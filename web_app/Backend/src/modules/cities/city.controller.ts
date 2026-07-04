import { Request, Response }
from 'express';

import cityService
from './city.service';

import {
  serializeBigInt
}
from '../../utils/bigintSerializer';

class CityController {

  async getByGovernorate(
    req: Request,
    res: Response
  ) {
    try {
      const governorateId =
        Number(
          req.params.governorateId
        );

      const cities =
        await cityService.getByGovernorate(
          governorateId
        );

      res.json(
        serializeBigInt(
          cities
        )
      );
    } catch (error: any) {
      res.status(500).json({
        success: false,
        message:
          error.message,
      });
    }
  }

  async create(
    req: Request,
    res: Response
  ) {
    try {
      const {
        name,
        governorateId,
      } = req.body;

      const city =
        await cityService.create(
          name,
          governorateId
        );

      res.status(201).json(
        serializeBigInt({
          success: true,
          city,
        })
      );
    } catch (error: any) {
      res.status(500).json({
        success: false,
        message:
          error.message,
      });
    }
  }
}

export default new CityController();