import express from "express";
import cors from "cors";
import helmet from "helmet";
import cookieParser from "cookie-parser";

(BigInt.prototype as any).toJSON = function () {
  return this.toString();
};

import authRoutes from "./modules/auth/auth.routes";
import countryRoutes from "./modules/countries/country.routes";
import governorateRoutes from "./modules/governorates/governorate.routes";
import cityRoutes from "./modules/cities/city.routes";
import categoryRoutes from "./modules/categories/category.routes";
import medicineRoutes from "./modules/medicines/medicine.routes";
import favoriteRoutes from "./modules/favorites/favorite.routes";
import pharmacyRoutes from "./modules/pharmacies/pharmacy.routes";
import statisticsRoutes from "./modules/statistics/statistics.routes";
import notificationRoutes from "./modules/notifications/notification.routes";
import searchRoutes from "./modules/search/search.routes";

const app = express();

app.use(helmet());

app.use(
  cors({
    origin: ["http://localhost:4200", "https://medi-search-eight.vercel.app"],
    credentials: true,
  }),
);

app.use(express.json());
app.use(cookieParser());

app.get("/", (req, res) => {
  res.json({
    success: true,
    message: "MediSearch API Running",
  });
});

app.get("/api/health", (req, res) => {
  res.json({
    success: true,
    message: "Server is healthy",
  });
});

app.use("/api/auth", authRoutes);
app.use("/api/categories", categoryRoutes);
app.use("/api/home/medicines", medicineRoutes);
app.use("/api/favorites", favoriteRoutes);
app.use("/api/countries", countryRoutes);
app.use("/api/governorates", governorateRoutes);
app.use("/api/cities", cityRoutes);
app.use("/api/home/pharmacies", pharmacyRoutes);
app.use("/api/home/statistics", statisticsRoutes);
app.use("/api/notifications", notificationRoutes);
app.use("/api/search", searchRoutes);
export default app;
