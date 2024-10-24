<script>import { MarkdownCode as Markdown } from "@gradio/markdown-code";
export let info;
export let root;
</script>

<div>
	<Markdown {root} message={info} sanitize_html={true} />
</div>

<style>
	div {
		margin-bottom: var(--spacing-lg);
		color: var(--block-info-text-color);
		font-weight: var(--block-info-text-weight);
		font-size: var(--block-info-text-size);
		line-height: var(--line-sm);
	}
</style>
