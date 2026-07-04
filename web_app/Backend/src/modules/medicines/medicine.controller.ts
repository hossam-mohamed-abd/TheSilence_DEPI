import {
  Request,
  Response,
} from 'express';

import { MedicineService }
from './medicine.service';

export class MedicineController {
  private medicineService =
    new MedicineService();

  getFeaturedMedicines =
    async (
      req: Request,
      res: Response
    ) => {
      try {
        const page =
          Number(
            req.query.page || 1
          );

        const result =
          await this
            .medicineService
            .getFeaturedMedicines(
              page
            );

        return res.json({
          success: true,
          hasMore:
            result.hasMore,
          data:
            result.medicines,
        });
      } catch (error: any) {
        console.error(error);

        return res
          .status(500)
          .json({
            success: false,
            message:
              error.message,
          });
      }
    };
}