import React from "react";

interface HeaderProps {
  sessionTitle?: string;
  isCollapsed?: boolean;
  onUploadClick?: () => void;
  activeDataFrameVersion?: string;
}

export const Header: React.FC<HeaderProps> = ({
  sessionTitle = "Q3 Revenue Cohort Analysis",
  isCollapsed = false,
  onUploadClick,
  activeDataFrameVersion = "df_v0",
}) => {
  return (
    <header
      className={`fixed top-0 right-0 h-16 bg-surface/85 backdrop-blur-xl z-40 px-space-lg flex items-center justify-between border-b border-outline-variant/15 transition-all duration-300 ${
        isCollapsed ? "left-16" : "left-64"
      }`}
    >
      {/* Left: Breadcrumbs */}
      <div className="flex items-center gap-space-sm font-body-sm text-body-sm text-on-surface-variant overflow-hidden">
        <span className="hover:text-on-surface transition-colors cursor-pointer shrink-0">
          Sessions
        </span>
        <span className="text-outline">/</span>
        <span className="text-on-surface font-body-md text-body-md font-medium truncate">
          {sessionTitle}
        </span>
        {activeDataFrameVersion && (
          <span className="px-2 py-0.5 rounded-full bg-primary-container/20 text-primary font-code-tabular text-[11px] font-medium shrink-0">
            {activeDataFrameVersion}
          </span>
        )}
      </div>

      {/* Right: Live Connection Pill, Nav & Actions */}
      <div className="flex items-center gap-space-md shrink-0">
        {/* Live BigQuery / DuckDB Connection Status */}
        <div className="hidden md:flex items-center gap-space-xs px-space-sm py-1 rounded-full bg-surface-container font-code-tabular text-code-tabular text-[12px] text-tertiary shadow-sm">
          <span className="w-2 h-2 rounded-full bg-tertiary animate-pulse"></span>
          <span>BigQuery Connected • 14ms</span>
        </div>

        {/* Upload Dataset Quick Trigger */}
        {onUploadClick && (
          <button
            onClick={onUploadClick}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-surface-container hover:bg-surface-container-high text-primary hover:text-primary-container transition-all font-body-sm text-body-sm shadow-sm"
          >
            <span className="material-symbols-outlined text-[16px]">upload_file</span>
            <span className="hidden sm:inline">Upload Data</span>
          </button>
        )}

        <nav className="hidden lg:flex items-center gap-space-md font-body-sm text-body-sm text-on-surface-variant">
          <a
            className="hover:text-on-surface transition-colors"
            href="https://cloud.google.com/bigquery/docs"
            target="_blank"
            rel="noreferrer"
          >
            Docs
          </a>
          <button
            onClick={onUploadClick}
            className="hover:text-on-surface transition-colors"
          >
            Integrations
          </button>
        </nav>

        <div className="flex items-center gap-1">
          <button
            className="w-8 h-8 rounded-full flex items-center justify-center text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface transition-colors"
            type="button"
            title="Notifications"
          >
            <span className="material-symbols-outlined text-[20px]">notifications</span>
          </button>
          <button
            className="w-8 h-8 rounded-full flex items-center justify-center text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface transition-colors"
            type="button"
            title="Share Workspace"
          >
            <span className="material-symbols-outlined text-[20px]">share</span>
          </button>
        </div>

        <img
          alt="Profile"
          className="w-8 h-8 rounded-full object-cover border border-primary/30"
          src="/assets/fares-avatar.png"
          onError={(e) => {
            (e.target as HTMLImageElement).src =
              "https://lh3.googleusercontent.com/aida-public/AB6AXuD3oGy_JtI9L39Rh0ZQjW6_1atfTh0851i8WrMZSIJqy8RVSYn29DT7-4qKnUIEi6YiPRaOuE5WMhwYJb314V2St3KPtSarppuKUxR0-JLtyyHgszshSv5QwOspA9Tfq9D-Zwh1xyvgbKaXdN-9E6E5PAjSPVslSm6lvo-22sWNYfikdyoavQb8ZRxeUloQTrwEGwt9F-GmhCfIJ5WzSWwrkGdh8Py13KiZvH3LxqTWDI72LoxsaP8i";
          }}
        />
      </div>
    </header>
  );
};
