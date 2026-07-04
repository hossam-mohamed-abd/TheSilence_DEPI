import prisma from "../../config/prisma";

export class CategoryRepository {
  async findAll() {
    const categories = await prisma.drug_categories.findMany({
      select: {
        id: true,
        name: true,
        description: true,
        image_url: true,
      },
      orderBy: {
        name: "asc",
      },
    });

    return categories.map((category) => ({
      ...category,
      id: Number(category.id),
    }));
  }

  async findHomeCategories() {
    const [categories, total] = await prisma.$transaction([
      prisma.drug_categories.findMany({
        where: {
          image_url: {
            not: null,
          },
        },
        take: 4,
        orderBy: {
          name: "asc",
        },
        select: {
          id: true,
          name: true,
          description: true,
          image_url: true,
        },
      }),

      prisma.drug_categories.count(),
    ]);

    return {
      total,
      remaining: Math.max(total - categories.length, 0),
      categories: categories.map((category) => ({
        ...category,
        id: Number(category.id),
      })),
    };
  }
}
