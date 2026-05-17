import { test, expect } from "@playwright/test";

test.describe("Teacher Flow - Request syllabus or teaching methodology guidance", () => {
  test("teacher can request a syllabus and receive structured content", async ({
    page,
  }) => {
    await page.goto("/");

    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();

    const textarea = page.getByRole("textbox");
    await expect(textarea).toBeVisible();
    await textarea.fill("Create a syllabus for G8 logarithms");

    const sendButton = page.locator(".send-button");
    await expect(sendButton).toBeVisible();
    await sendButton.click();

    await expect(page.getByText("Create a syllabus for G8 logarithms")).toBeVisible({ timeout: 10000 });

    const responseBubble = page.locator(".message.assistant").last();
    await expect(responseBubble).toBeVisible({ timeout: 60000 });
  });

  test("teacher can request teaching methodology guidance", async ({ page }) => {
    await page.goto("/");

    const textarea = page.getByRole("textbox");
    await textarea.fill("What is the best teaching methodology for fractions?");
    await page.locator(".send-button").click();

    await expect(page.locator(".message")).toHaveCount(2, { timeout: 60000 });
  });

  test("teacher can request lesson plan with NHM alignment", async ({
    page,
  }) => {
    await page.goto("/");

    const textarea = page.getByRole("textbox");
    await textarea.fill(
      "Create a lesson plan for geometry following NHM principles"
    );
    await page.locator(".send-button").click();

    const responseBubble = page.locator(".message.assistant").last();
    await expect(responseBubble).toBeVisible({ timeout: 60000 });
  });

  test("teacher can continue conversation about curriculum", async ({
    page,
  }) => {
    await page.goto("/");

    const textarea = page.getByRole("textbox");
    await textarea.fill("Design a curriculum for G9 algebra");
    await page.locator(".send-button").click();

    await expect(page.locator(".message")).toHaveCount(2, { timeout: 60000 });

    await textarea.fill("How should I pace this over a semester?");
    await expect(page.locator(".send-button")).toBeEnabled({ timeout: 60000 });
    await page.locator(".send-button").click();

    await expect(page.locator(".message")).toHaveCount(4, { timeout: 60000 });
  });
});
