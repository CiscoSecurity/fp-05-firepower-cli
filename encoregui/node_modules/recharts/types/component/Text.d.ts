import React, { CSSProperties, SVGProps } from 'react';
interface TextProps {
    scaleToFit?: boolean;
    angle?: number;
    textAnchor?: 'start' | 'middle' | 'end' | 'inherit';
    verticalAnchor?: 'start' | 'middle' | 'end';
    style?: CSSProperties;
    lineHeight?: number | string;
    breakAll?: boolean;
    children?: string | number;
    maxLines?: number;
}
export declare type Props = Omit<SVGProps<SVGTextElement>, 'textAnchor' | 'verticalAnchor'> & TextProps;
export declare const Text: {
    (props: Props): React.JSX.Element;
    defaultProps: {
        x: number;
        y: number;
        lineHeight: string;
        capHeight: string;
        scaleToFit: boolean;
        textAnchor: string;
        verticalAnchor: string;
        fill: string;
    };
};
export {};
