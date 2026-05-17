import { useRef, useState, useCallback } from "react";

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
const ACCEPTED_TYPES = ["image/png", "image/jpeg", "image/webp"];

interface ImageUploadProps {
  onImagesChange: (files: File[]) => void;
  images: File[];
}

export function ImageUpload({ onImagesChange, images }: ImageUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [previews, setPreviews] = useState<string[]>([]);
  const [error, setError] = useState<string>("");

  const generatePreviews = useCallback((files: File[]) => {
    const urls = files.map((f) => URL.createObjectURL(f));
    setPreviews(urls);
    return urls;
  }, []);

  const handleFiles = useCallback(
    (files: File[]) => {
      setError("");
      const validFiles = files.filter((f) => {
        if (!ACCEPTED_TYPES.includes(f.type)) {
          setError(`不支持的格式：${f.name}`);
          return false;
        }
        if (f.size > MAX_FILE_SIZE) {
          setError(`文件过大：${f.name}（最大10MB）`);
          return false;
        }
        return true;
      });
      onImagesChange(validFiles);
      generatePreviews(validFiles);
    },
    [onImagesChange, generatePreviews]
  );

  const handleClick = () => inputRef.current?.click();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    handleFiles(files);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    const files = Array.from(e.dataTransfer.files);
    handleFiles(files);
  };

  const removeImage = (index: number) => {
    if (previews[index]) {
      URL.revokeObjectURL(previews[index]);
    }
    const newFiles = images.filter((_, i) => i !== index);
    const newPreviews = previews.filter((_, i) => i !== index);
    onImagesChange(newFiles);
    setPreviews(newPreviews);
  };

  return (
    <div className="image-upload-container">
      <div
        className={`drop-zone ${isDragging ? "dragging" : ""} ${images.length > 0 ? "has-images" : ""}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <input
          ref={inputRef}
          type="file"
          accept={ACCEPTED_TYPES.join(",")}
          multiple
          style={{ display: "none" }}
          onChange={handleChange}
        />
        {images.length === 0 ? (
          <div className="drop-zone-placeholder">
            <span className="drop-zone-icon">📷</span>
            <span className="drop-zone-text">拖拽图片或点击上传</span>
            <span className="drop-zone-hint">PNG、JPG、WebP格式，最大10MB</span>
          </div>
        ) : (
          <div className="preview-grid">
            {previews.map((url, index) => (
              <div key={index} className="preview-item">
                <img src={url} alt={`预览 ${index + 1}`} className="preview-image" />
                <button
                  type="button"
                  className="preview-remove"
                  onClick={(e) => {
                    e.stopPropagation();
                    removeImage(index);
                  }}
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
      {error && <div className="upload-error">{error}</div>}
    </div>
  );
}
