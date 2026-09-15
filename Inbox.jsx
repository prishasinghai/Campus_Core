import React, { useState, useEffect, useCallback } from 'react';
import { base44 } from '@/api/base44Client';
import Importer from '@/components/Importer';
import { PageHeader, EmptyState, SectionHeader } from '@/components/ui-shared';
import ItemCard from '@/components/ItemCard';
import { Eye, X } from 'lucide-react';

export default function Inbox() {
  const [items, setItems] = useState([]);
  const [announcements, setAnnouncements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sourceItem, setSourceItem] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [its, anns] = await Promise.all([
        base44.entities.Item.list('-created_date', 100),
        base44.entities.Announcement.list('-imported_date', 50),
      ]);
      setItems(its);
      setAnnouncements(anns);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const toggleDone = async (item) => {
    const newStatus = item.status === 'done' ? 'todo' : 'done';
    setItems(items.map(i => i.id === item.id ? { ...i, status: newStatus } : i));
    await base44.entities.Item.update(item.id, { status: newStatus });
  };

  return (
    <div>
      <PageHeader title="Inbox" subtitle="Drop in the chaos. Get back a clear plan." />

      <Importer onImported={load} />

      <SectionHeader title="Extracted items" subtitle="Everything the AI has pulled from your announcements." icon="✓" />

      {loading ? (
        <div className="space-y-3">
          {[1,2,3].map(i => <div key={i} className="h-32 rounded-[1.25rem] shimmer" />)}
        </div>
      ) : items.length === 0 ? (
        <EmptyState icon="✦" title="Nothing here yet" subtitle="Paste an announcement above to get started." />
      ) : (
        <div className="grid gap-3 md:grid-cols-2">
          {items.map(item => (
            <ItemCard key={item.id} item={item} onToggleDone={toggleDone} onViewSource={setSourceItem} compact />
          ))}
        </div>
      )}

      {announcements.length > 0 && (
        <>
          <SectionHeader title="Raw announcements" subtitle="The original messages you've imported." icon="📋" />
          <div className="space-y-2">
            {announcements.map(a => (
              <div key={a.id} className="editorial-card p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-semibold text-primary">📍 {a.source}</span>
                  <span className="text-[10px] text-muted-foreground">{new Date(a.imported_date || a.created_date).toLocaleString()}</span>
                </div>
                <p className="text-sm text-foreground/70 whitespace-pre-wrap line-clamp-4">{a.raw_text}</p>
              </div>
            ))}
          </div>
        </>
      )}

      {sourceItem && (
        <SourceModal item={sourceItem} onClose={() => setSourceItem(null)} />
      )}
    </div>
  );
}

export function SourceModal({ item, onClose }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm" onClick={onClose}>
      <div className="bg-card rounded-[1.5rem] max-w-lg w-full p-6 animate-float-up" onClick={e => e.stopPropagation()}>
        <div className="flex items-start justify-between mb-4">
          <div>
            <p className="text-[10px] uppercase tracking-wider text-muted-foreground">Original source</p>
            <h3 className="font-heading text-xl font-semibold text-primary">{item.title}</h3>
          </div>
          <button onClick={onClose} className="p-1.5 rounded-full hover:bg-muted"><X className="w-4 h-4" /></button>
        </div>
        <div className="p-4 rounded-xl bg-muted/60 border border-border">
          <p className="text-xs text-muted-foreground mb-2 flex items-center gap-1.5"><Eye className="w-3 h-3" /> Extracted from:</p>
          <p className="text-sm text-foreground/80 whitespace-pre-wrap font-mono leading-relaxed">{item.raw_source_text}</p>
        </div>
        <div className="mt-3 text-xs text-muted-foreground">📍 {item.source}</div>
      </div>
    </div>
  );
}
