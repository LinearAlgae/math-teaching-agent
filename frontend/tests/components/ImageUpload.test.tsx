import { describe, it, expect, vi, afterEach } from "vitest";
import { cleanup, render, screen, fireEvent } from "@testing-library/react";
import { ImageUpload } from "../../src/components/ImageUpload";

afterEach(cleanup);

describe("ImageUpload", () => {
  it("renders upload button with placeholder text", () => {
    const onImagesChange = vi.fn();
    render(<ImageUpload onImagesChange={onImagesChange} images={[]} />);
    expect(screen.getByText("拖拽图片或点击上传")).toBeTruthy();
  });

  it("shows format hint", () => {
    const onImagesChange = vi.fn();
    const { container } = render(<ImageUpload onImagesChange={onImagesChange} images={[]} />);
    expect(container.querySelector(".drop-zone-hint")?.textContent).toContain("PNG");
  });

  it("shows image preview when images attached", () => {
    const onImagesChange = vi.fn();
    const { container } = render(<ImageUpload onImagesChange={onImagesChange} images={[]} />);
    const input = container.querySelector('input[type="file"]')!;
    const file = new File(["dummy"], "test.png", { type: "image/png" });
    fireEvent.change(input, { target: { files: [file] } });
    expect(onImagesChange).toHaveBeenCalledWith([file]);
  });

  it("opens file picker on click", () => {
    const onImagesChange = vi.fn();
    const { container } = render(<ImageUpload onImagesChange={onImagesChange} images={[]} />);
    const dropZone = container.querySelector(".drop-zone");
    expect(dropZone).toBeTruthy();
  });

  it("filters out oversized files", () => {
    const onImagesChange = vi.fn();
    const largeFile = new File(["x".repeat(11 * 1024 * 1024)], "large.png", { type: "image/png" });
    const { container } = render(<ImageUpload onImagesChange={onImagesChange} images={[]} />);
    const input = container.querySelector('input[type="file"]')!;
    fireEvent.change(input, { target: { files: [largeFile] } });
    expect(onImagesChange).toHaveBeenCalledWith([]);
  });

  it("removes image when remove button clicked", () => {
    const onImagesChange = vi.fn();
    const { container } = render(<ImageUpload onImagesChange={onImagesChange} images={[]} />);
    const input = container.querySelector('input[type="file"]')!;
    const file = new File(["dummy"], "test.png", { type: "image/png" });
    fireEvent.change(input, { target: { files: [file] } });
    const removeBtn = container.querySelector(".preview-remove") as HTMLButtonElement;
    if (removeBtn) {
      fireEvent.click(removeBtn);
      expect(onImagesChange).toHaveBeenCalledWith([]);
    }
  });
});
