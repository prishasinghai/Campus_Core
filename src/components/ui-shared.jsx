import React from 'react';

export function PageHeader({ title, subtitle }) {
  return (
    <div className="mb-6">
      <h1 className="text-3xl font-bold tracking-tight text-primary mb-1">{title}</h1>
      <p className="text-muted-foreground text-sm">{subtitle}</p>
    </div>
  );
}

export function SectionHeader({ title, subtitle, icon }) {
  return (
    <div className="flex items-center gap-2 mt-8 mb-4">
      {icon && <span className="text-lg">{icon}</span>}
      <div>
        <h2 className="text-lg font-semibold text-foreground">{title}</h2>
        <p className="text-xs text-muted-foreground">{subtitle}</p>
      </div>
    </div>
  );
}

export function EmptyState({ title, subtitle, icon }) {
  return (
    <div className="flex flex-col items-center justify-center p-8 border border-dashed rounded-2xl text-center my-4 bg-muted/20">
      <span className="text-3xl mb-2">{icon}</span>
      <h3 className="font-semibold text-foreground">{title}</h3>
      <p className="text-xs text-muted-foreground max-w-xs mt-1">{subtitle}</p>
    </div>
  );
}

