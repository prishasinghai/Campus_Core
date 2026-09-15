import React, { useState } from 'react';

export default function Importer({ onImported }) {
  const [text, setText] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;

    setSubmitting(true);
    try {
      // In a real app, this sends the data to your AI backend
      console.log("Importing text:", text);
      setText('');
      if (onImported) onImported();
    } catch (error) {
      console.error(error);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6 p-4 bg-muted/30 border border-border rounded-[1.25rem]">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Paste a chaotic announcement or message here..."
        className="w-full h-24 p-3 text-sm rounded-xl border border-border bg-background focus:outline-none focus:ring-1 focus:ring-primary resize-none"
        disabled={submitting}
      />
      <div className="flex justify-end mt-2">
        <button
          type="submit"
          disabled={submitting || !text.trim()}
          className="px-4 py-2 text-xs font-medium text-white bg-black rounded-xl hover:bg-black/80 disabled:opacity-50 transition-colors"
        >
          {submitting ? 'Processing with AI...' : 'Scan Announcement ✨'}
        </button>
      </div>
    </form>
  );
}

