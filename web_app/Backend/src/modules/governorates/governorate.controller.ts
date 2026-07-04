import { Request, Response } from 'express';

import governorateService from './governorate.service';

import { serializeBigInt }
from '../../utils/bigintSerializer';

class GovernorateController {

  async getByCountry(
    req: Request,
    res: Response
  ) {
    try {
      const countryId = Number(
        req.params.countryId
      );

      const governorates =
        await governorateService.getByCountry(
          countryId
        );

      res.json(
        serializeBigInt(
          governorates
        )
      );
    } catch (error: any) {
      res.status(500).json({
        success: false,
        message: error.message,
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
        countryId,
      } = req.body;

      const governorate =
        await governorateService.create(
          name,
          countryId
        );

      res.status(201).json(
        serializeBigInt({
          success: true,
          governorate,
        })
      );
    } catch (error: any) {
      res.status(500).json({
        success: false,
        message: error.message,
      });
    }
  }
}

export default new GovernorateController();