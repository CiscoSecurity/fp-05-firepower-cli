import React, { CSSProperties, ReactNode, ReactElement, SVGProps } from 'react';
import { ValueType, NameType, Payload, Props as DefaultProps } from './DefaultTooltipContent';
import { AnimationTiming } from '../util/types';
export declare type ContentType<TValue extends ValueType, TName extends NameType> = ReactElement | ((props: TooltipProps<TValue, TName>) => ReactNode);
declare type UniqueFunc<TValue extends ValueType, TName extends NameType> = (entry: Payload<TValue, TName>) => unknown;
declare type UniqueOption<TValue extends ValueType, TName extends NameType> = boolean | UniqueFunc<TValue, TName>;
export declare type TooltipProps<TValue extends ValueType, TName extends NameType> = DefaultProps<TValue, TName> & {
    allowEscapeViewBox?: {
        x?: boolean;
        y?: boolean;
    };
    reverseDirection?: {
        x?: boolean;
        y?: boolean;
    };
    content?: ContentType<TValue, TName>;
    viewBox?: {
        x?: number;
        y?: number;
        width?: number;
        height?: number;
    };
    active?: boolean;
    offset?: number;
    wrapperStyle?: CSSProperties;
    cursor?: boolean | ReactElement | SVGProps<SVGElement>;
    coordinate?: {
        x?: number;
        y?: number;
    };
    position?: {
        x?: number;
        y?: number;
    };
    trigger?: 'hover' | 'click';
    shared?: boolean;
    payloadUniqBy?: UniqueOption<TValue, TName>;
    isAnimationActive?: boolean;
    animationDuration?: number;
    animationEasing?: AnimationTiming;
    filterNull?: boolean;
    useTranslate3d?: boolean;
};
export declare const Tooltip: {
    <TValue extends ValueType, TName extends string | number>(props: DefaultProps<TValue, TName> & {
        allowEscapeViewBox?: {
            x?: boolean;
            y?: boolean;
        };
        reverseDirection?: {
            x?: boolean;
            y?: boolean;
        };
        content?: ContentType<TValue, TName>;
        viewBox?: {
            x?: number;
            y?: number;
            width?: number;
            height?: number;
        };
        active?: boolean;
        offset?: number;
        wrapperStyle?: CSSProperties;
        cursor?: boolean | ReactElement | SVGProps<SVGElement>;
        coordinate?: {
            x?: number;
            y?: number;
        };
        position?: {
            x?: number;
            y?: number;
        };
        trigger?: 'hover' | 'click';
        shared?: boolean;
        payloadUniqBy?: UniqueOption<TValue, TName>;
        isAnimationActive?: boolean;
        animationDuration?: number;
        animationEasing?: AnimationTiming;
        filterNull?: boolean;
        useTranslate3d?: boolean;
    } & {
        children?: React.ReactNode;
    }): React.JSX.Element;
    displayName: string;
    defaultProps: TooltipProps<number, string>;
};
export {};
