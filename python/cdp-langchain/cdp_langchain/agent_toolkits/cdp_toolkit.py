"""CDP Toolkit."""

from langchain_core.tools import BaseTool
from langchain_core.tools.base import BaseToolkit

from cdp_agentkit_core.actions import CDP_ACTIONS
from cdp_langchain.tools import CdpTool
from cdp_langchain.utils import CdpAgentkitWrapper


class CdpToolkit(BaseToolkit):
    """Coinbase Developer Platform (CDP) Toolkit.

    *Security Note*: This toolkit contains tools that can read and modify
        the state of a service; e.g., by creating, deleting, or updating,
        reading underlying data.

        For example, this toolkit can be used to create wallets, transactions,
        and smart contract invocations on CDP supported blockchains.

        See [Security](https://python.langchain.com/docs/security) for more information.

    Setup:
        See detailed installation instructions here:
        https://python.langchain.com/docs/integrations/tools/cdp/#installation

        You will need to set the following environment
        variables:

        .. code-block:: bash

            export CDP_API_KEY_NAME="cdp-api-key-name"
            export CDP_API_KEY_PRIVATE_KEY="cdp-api-key-private-key" 
            export NETWORK_ID="network-id"
            export CDP_MODEL_NAME="gpt-4o-mini"       # Optional
            export CDP_MODEL_PROVIDER="openai"         # Optional
            export OPENAI_API_KEY="your-api-key"       # Required for OpenAI
            export ANTHROPIC_API_KEY="your-api-key"    # Required for Anthropic  
            export CEREBRAS_API_KEY="your-api-key"     # Required for Cerebras

    Instantiate:
        .. code-block:: python

            from cdp_langchain.agent_toolkits import CdpToolkit
            from cdp_langchain.utils import CdpAgentkitWrapper

            # Custom model configuration
            cdp = CdpAgentkitWrapper(
                model_name="claude-3-sonnet",
                provider="anthropic"
            )
            cdp_toolkit = CdpToolkit.from_cdp_agentkit_wrapper(cdp)

    Tools:
        .. code-block:: python

            tools = cdp_toolkit.get_tools()
            for tool in tools:
                print(tool.name)

        .. code-block:: none

            get_wallet_details
            get_balance
            get_balance_nft
            request_faucet_funds
            transfer
            transfer_nft
            trade
            deploy_token
            mint_nft
            deploy_nft
            deploy_contract
            register_basename
            wow_create_token
            wow_buy_token
            wow_sell_token
            wrap_eth
    Use within an agent:
        .. code-block:: python

            from langchain_openai import ChatOpenAI
            from langgraph.prebuilt import create_react_agent

            # Select example tool
            tools = [tool for tool in toolkit.get_tools() if tool.name == "get_wallet_details"]
            assert len(tools) == 1

            # Dynamic LLM initialization based on provider
            if cdp_agentkit_wrapper.provider == "openai":
                from langchain_openai import ChatOpenAI
                llm = ChatOpenAI(
                    model=cdp_agentkit_wrapper.model_name,
                    openai_api_key=os.getenv("OPENAI_API_KEY")
                )
            elif cdp_agentkit_wrapper.provider == "anthropic":
                from langchain_anthropic import ChatAnthropic
                llm = ChatAnthropic(
                    model=cdp_agentkit_wrapper.model_name,
                    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
                )
            elif cdp_agentkit_wrapper.provider == "cerebras":
                from langchain_cerebras import ChatCerebras
                llm = ChatCerebras(
                    model=cdp_agentkit_wrapper.model_name,
                    cerebras_api_key=os.getenv("CEREBRAS_API_KEY")
                )
            else:
                raise ValueError(f"Unsupported provider: {cdp_agentkit_wrapper.provider}")
            agent_executor = create_react_agent(llm, tools)

            example_query = "Tell me about your wallet"

            events = agent_executor.stream(
                {"messages": [("user", example_query)]},
                stream_mode="values",
            )
            for event in events:
                event["messages"][-1].pretty_print()

        .. code-block:: none

             ================================[1m Human Message [0m=================================

            Tell me about your wallet
            ==================================[1m Ai Message [0m==================================
            Tool Calls:
            get_wallet_details (call_iSYJVaM7uchfNHOMJoVPQsOi)
            Call ID: call_iSYJVaM7uchfNHOMJoVPQsOi
            Args:
                no_input: ""
            =================================[1m Tool Message [0m=================================
            Name: get_wallet_details

            ...
            ==================================[1m Ai Message [0m==================================

            My wallet is wallet-id-123 on Base Sepolia with default address 0x0123

    Parameters
    ----------
        tools: List[BaseTool]. The tools in the toolkit. Default is an empty list.

    """

    tools: list[BaseTool] = []  # noqa: RUF012

    @classmethod
    def from_cdp_agentkit_wrapper(cls, cdp_agentkit_wrapper: CdpAgentkitWrapper) -> "CdpToolkit":
        """Create a CdpToolkit from a CdpAgentkitWrapper.

        Args:
            cdp_agentkit_wrapper: CdpAgentkitWrapper. The CDP Agentkit wrapper.

        Returns:
            CdpToolkit. The CDP toolkit.

        """
        actions = CDP_ACTIONS

        tools = [
            CdpTool(
                name=action.name,
                description=action.description,
                cdp_agentkit_wrapper=cdp_agentkit_wrapper,
                args_schema=action.args_schema,
                func=action.func,
            )
            for action in actions
        ]

        return cls(tools=tools)  # type: ignore[arg-type]

    def get_tools(self) -> list[BaseTool]:
        """Get the tools in the toolkit."""
        return self.tools
