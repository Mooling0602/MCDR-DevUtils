import json
import copy

# 尝试导入 prompt_toolkit，如果导入失败则使用内置 input
try:
    from prompt_toolkit import prompt
    use_prompt_toolkit = True
except ImportError:
    use_prompt_toolkit = False

# 模板内容
meta_template = {
    "id": "plugin_id",
    "version": "0.0.1",
    "name": "Plugin",
    "description": {
        "en_us": "Description of this plugin.",
        "zh_cn": "此插件的介绍。"
    },
    "author": "Unknown",
    "link": "https://github.com",
    "dependencies": {
        "mcdreforged": ">=2.14.1"
    },
    "entrypoint": None,  # Optional
    "resources": ["lang"]  # Optional
}

def get_input(prompt_text, default):
    """
    提示用户输入，如果用户输入为空，则返回默认值。
    使用 prompt_toolkit 时可以享受更好的编辑体验。
    """
    default_str = str(default) if default is not None else ""
    full_prompt = f"{prompt_text} (默认: {default_str}): "
    if use_prompt_toolkit:
        user_input = prompt(full_prompt, default=default_str)
    else:
        user_input = input(full_prompt)
    if user_input.strip() == "":
        return default
    return user_input

def main():
    # 深拷贝模板，避免修改原始模板
    meta = copy.deepcopy(meta_template)

    # 依次询问用户信息，并保留默认值（模板内容）作为后备值
    meta["id"] = get_input("请输入插件 id", meta["id"])
    meta["version"] = get_input("请输入插件版本", meta["version"])
    meta["name"] = get_input("请输入插件名称", meta["name"])
    meta["description"]["en_us"] = get_input("请输入英文描述", meta["description"]["en_us"])
    meta["description"]["zh_cn"] = get_input("请输入中文描述", meta["description"]["zh_cn"])
    meta["author"] = get_input("请输入作者", meta["author"])
    meta["link"] = get_input("请输入链接", meta["link"])
    meta["dependencies"]["mcdreforged"] = get_input("请输入 mcdreforged 依赖版本", meta["dependencies"]["mcdreforged"])
    
    # entrypoint 字段，允许为空（保留模板的 None）
    entrypoint_input = get_input("请输入 entrypoint (可选)", meta["entrypoint"])
    if entrypoint_input != "" and entrypoint_input is not None:
        meta["entrypoint"] = entrypoint_input
    else:
        del meta["entrypoint"]

    # 资源列表处理，默认值为模板中的列表
    resources_default = ", ".join(meta["resources"]) if meta["resources"] else ""
    resources_input = get_input("请输入资源列表（使用逗号分隔，可选）", resources_default)
    if resources_input.strip() == "":
        meta["resources"] = meta_template["resources"]
    else:
        meta["resources"] = [item.strip() for item in resources_input.split(",") if item.strip()]

    # 输出文件名
    output_filename = "mcdreforged.plugin.json"
    
    # 写入 JSON 文件（确保中文不会被转义）
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=4)
    
    print(f"成功生成 JSON 文件：{output_filename}")