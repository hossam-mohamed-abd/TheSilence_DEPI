import { Request, Response } from "express";

import { SearchService } from "./search.service";

const service = new SearchService();

export class SearchController {
  search = async (req: Request, res: Response) => {
    try {
      const q = String(req.query.q ?? "");

      const page = Number(req.query.page) || 1;

      const limit = Number(req.query.limit) || 12;

      const data = await service.search(q, page, limit);

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
}
