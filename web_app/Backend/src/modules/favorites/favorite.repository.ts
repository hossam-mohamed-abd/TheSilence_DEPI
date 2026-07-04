import prisma from "../../config/prisma";

export class FavoriteRepository {
  async addFavorite(userId: bigint, drugId: bigint) {
    return prisma.favorites.create({
      data: {
        user_id: userId,
        drug_id: drugId,
      },
    });
  }

  async removeFavorite(userId: bigint, drugId: bigint) {
    return prisma.favorites.delete({
      where: {
        user_id_drug_id: {
          user_id: userId,
          drug_id: drugId,
        },
      },
    });
  }

  async findFavorite(userId: bigint, drugId: bigint) {
    return prisma.favorites.findUnique({
      where: {
        user_id_drug_id: {
          user_id: userId,
          drug_id: drugId,
        },
      },
    });
  }
  async getFavorites(userId: bigint) {
    const favorites = await prisma.favorites.findMany({
      where: {
        user_id: userId,
      },

      include: {
        drugs: {
          include: {
            drug_categories: true,
            pharmacy_inventory: true,
            drug_alternatives_drug_alternatives_drug_idTodrugs: true,
          },
        },
      },

      orderBy: {
        created_at: "desc",
      },
    });

    return favorites
      .filter((f) => f.drugs)
      .map((f) => ({
        ...f.drugs,
        is_favorite: true,
        category_name: f.drugs?.drug_categories?.name,

        pharmacy_count: f.drugs?.pharmacy_inventory?.length ?? 0,

        alternatives_count:
          f.drugs?.drug_alternatives_drug_alternatives_drug_idTodrugs?.length ??
          0,

        min_price: f.drugs?.pharmacy_inventory?.length
          ? Math.min(...f.drugs.pharmacy_inventory.map((p) => Number(p.price)))
          : null,

        is_available:
          f.drugs?.pharmacy_inventory?.some((p) => (p.quantity ?? 0) > 0) ??
          false,
      }));
  }
  async countFavorites(userId: bigint) {
    return prisma.favorites.count({
      where: {
        user_id: userId,
      },
    });
  }
}
