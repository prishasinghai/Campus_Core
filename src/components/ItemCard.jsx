import React from 'react';
import { Eye } from 'lucide-react';

export default function ItemCard({ item, onToggleDone, onViewSource, compact }) {
  const isDone = item.status === 'done';

  return (
    <div className={`p-4 rounded-[1.25rem] border transition-all ${isDone ? 'bg-muted/40 border-muted opacity-60' : 'bg-card border-border shadow-sm'}`}>
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-2.5">
          <input 
            type="checkbox" 
            checked={isDone} 
            onChange={() => onToggleDone(item)}
            className="mt-1 h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
          />
          <div>
            <h4 className={`font-medium text-sm ${isDone ? 'line-through text-muted-foreground' : 'text-foreground'}`}>
              {item.title || 'Untitled Item'}
            </h4>
            {!compact && <p className="text-xs text-muted-foreground mt-1">{item.description}</p>}
          </div>
        </div>
        
        <button 
          onClick={() => onViewSource(item)}
          className="p-1 text-muted-foreground hover:text-foreground rounded-md hover:bg-muted transition-colors"
          title="View Original Source"
        >
          <Eye className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}

