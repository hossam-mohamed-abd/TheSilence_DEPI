import { Request, Response } from "express";

import { PharmacyService } from "./pharmacy.service";

const service = new PharmacyService();

export class PharmacyController {
  async getFeaturedPharmacies(req: Request, res: Response) {
    try {
      const page = Number(req.query.page) || 1;

      const data = await service.getFeaturedPharmacies(page);

      res.json({
        success: true,
        data,
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        message: error.message,
      });
    }
  }

  private pharmacyService = new PharmacyService();

  getPharmacy = async (req: Request, res: Response) => {
    try {
      const id = BigInt(req.params.id as string);

      const pharmacy = await this.pharmacyService.getPharmacyDetails(id);

      return res.json({
        success: true,
        data: pharmacy,
      });
    } catch (error: any) {
      return res.status(404).json({
        success: false,
        message: error.message,
      });
    }
  };

  getPharmacyMedicines = async (
    req: Request<{ id: string }>,
    res: Response,
  ) => {
    try {
      const pharmacyId = BigInt(req.params.id);

      const page = Number(req.query.page) || 1;

      const limit = Number(req.query.limit) || 12;

      const search = String(req.query.search || "");

      const category = req.query.category
        ? BigInt(String(req.query.category))
        : undefined;

      const available = req.query.available === "true";

      const sort = String(req.query.sort || "name_asc");

      const result = await this.pharmacyService.getPharmacyMedicines(
        pharmacyId,
        {
          page,
          limit,
          search,
          category,
          available,
          sort,
        },
      );

      return res.json({
        success: true,
        ...result,
      });
    } catch (error: any) {
      return res.status(500).json({
        success: false,
        message: error.message,
      });
    }
  };

  getPharmacyCategories = async (
    req: Request<{ id: string }>,
    res: Response,
  ) => {
    try {
      const pharmacyId = BigInt(req.params.id);

      const data = await this.pharmacyService.getPharmacyCategories(pharmacyId);

      res.json({
        success: true,
        data,
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        message: error.message,
      });
    }
  };

  getPharmacyReviews = async (req: Request<{ id: string }>, res: Response) => {
    try {
      const pharmacyId = BigInt(req.params.id);

      const page = Number(req.query.page) || 1;

      const data = await this.pharmacyService.getPharmacyReviews(
        pharmacyId,
        page,
      );

      res.json({
        success: true,
        ...data,
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        message: error.message,
      });
    }
  };

  getPharmacyStatistics = async (
    req: Request<{ id: string }>,
    res: Response,
  ) => {
    try {
      const pharmacyId = BigInt(req.params.id);

      const data = await this.pharmacyService.getPharmacyStatistics(pharmacyId);

      res.json({
        success: true,
        data,
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        message: error.message,
      });
    }
  };

  addReview = async (req: Request<{ id: string }>, res: Response) => {
    try {
      const pharmacyId = BigInt(req.params.id);

      const userId = BigInt(req.user.id);

      const { rating, review } = req.body;

      await this.pharmacyService.addReview(pharmacyId, userId, rating, review);

      res.status(201).json({
        success: true,
      });
    } catch (error: any) {
      res.status(400).json({
        success: false,
        message: error.message,
      });
    }
  };
}
